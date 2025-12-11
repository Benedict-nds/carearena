"""Scheduler service with APScheduler jobs."""

from datetime import datetime, time as dt_time
from typing import List, Optional
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from app.db.database import SessionLocal
from app.db.models.scheduling import ScheduledCall, CallStatus
from app.db.models.patient import Patient
from app.db.models.schedule_preference import SchedulePreference
from app.db.models.hospital import Hospital
from app.db.models.enrollment import EnrollmentSyncLog, SyncStatus
from app.services.call_service import CallService
from app.services.csv_importer import CSVImporterService
from app.workflows.sms_flow import SMSFlow
from app.workflows.whatsapp_flow import WhatsAppFlow
from app.db.models.conversation import ConversationSession, SessionStatus
import pytz


class SchedulerService:
    """Service for scheduling jobs with APScheduler."""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.call_service = CallService()
    
    def setup_jobs(self):
        """Setup all scheduled jobs."""
        # Daily content delivery at preferred times
        self.scheduler.add_job(
            self.send_daily_content,
            trigger=CronTrigger(hour=8, minute=0),  # 8 AM daily
            id='daily_content_delivery',
            name='Send daily content at preferred times',
            replace_existing=True
        )
        
        # Weekly hospital sync
        self.scheduler.add_job(
            self.weekly_hospital_sync,
            trigger=CronTrigger(day_of_week='monday', hour=2, minute=0),  # Monday 2 AM
            id='weekly_hospital_sync',
            name='Weekly hospital CSV sync',
            replace_existing=True
        )
        
        # Automatic retries for missed calls (every hour)
        self.scheduler.add_job(
            self.retry_missed_calls,
            trigger=CronTrigger(minute=0),  # Every hour
            id='retry_missed_calls',
            name='Retry missed calls',
            replace_existing=True
        )
        
        # Cleanup job (delete expired audio/transcripts) - daily at 3 AM
        self.scheduler.add_job(
            self.cleanup_expired_assets,
            trigger=CronTrigger(hour=3, minute=0),
            id='cleanup_expired_assets',
            name='Cleanup expired audio/transcripts',
            replace_existing=True
        )
    
    def send_daily_content(self):
        """Send content at patient's preferred time."""
        db = SessionLocal()
        try:
            # Get all active patients with schedule preferences
            preferences = db.query(SchedulePreference).filter(
                SchedulePreference.is_active == True
            ).all()
            
            current_time = datetime.now(pytz.timezone('Africa/Accra'))
            current_hour = current_time.hour
            current_minute = current_time.minute
            
            for preference in preferences:
                if not preference.preferred_time:
                    continue
                
                # Check if it's the preferred time
                pref_hour = preference.preferred_time.hour
                pref_minute = preference.preferred_time.minute
                
                if current_hour == pref_hour and current_minute == pref_minute:
                    # Send content based on channel preference
                    if preference.channel_preference == "ivr":
                        self._schedule_ivr_call(db, preference.patient_id)
                    elif preference.channel_preference == "sms":
                        self._send_sms_content(db, preference.patient_id)
                    elif preference.channel_preference == "whatsapp":
                        self._send_whatsapp_content(db, preference.patient_id)
        finally:
            db.close()
    
    def weekly_hospital_sync(self):
        """Weekly hospital CSV sync."""
        db = SessionLocal()
        try:
            hospitals = db.query(Hospital).all()
            
            for hospital in hospitals:
                # TODO: Fetch CSV from hospital's endpoint or file system
                # For now, create a sync log entry
                sync_log = EnrollmentSyncLog(
                    hospital_id=hospital.id,
                    filename=f"weekly_sync_{datetime.now().strftime('%Y%m%d')}.csv",
                    total_rows=0,
                    status=SyncStatus.PENDING
                )
                db.add(sync_log)
                db.commit()
                
                # TODO: Process CSV import
                # importer = CSVImporterService()
                # result = importer.import_patients_from_csv(db, hospital.id, csv_path)
        finally:
            db.close()
    
    def retry_missed_calls(self):
        """Retry missed calls with exponential backoff."""
        db = SessionLocal()
        try:
            # Get failed calls that haven't exceeded max retries
            failed_calls = db.query(ScheduledCall).filter(
                ScheduledCall.status == CallStatus.FAILED,
                ScheduledCall.retry_count < ScheduledCall.max_retries
            ).all()
            
            for call in failed_calls:
                # Check if enough time has passed since last attempt
                time_since_last = datetime.utcnow() - call.updated_at
                hours_since = time_since_last.total_seconds() / 3600
                
                # Exponential backoff: 1h, 2h, 4h
                required_hours = 2 ** call.retry_count
                
                if hours_since >= required_hours:
                    # Retry the call
                    call.retry_count += 1
                    call.status = CallStatus.SCHEDULED
                    call.scheduled_time = datetime.utcnow()
                    db.commit()
                    
                    # Initiate call
                    self.call_service.initiate_call(call.patient, call)
        finally:
            db.close()
    
    def cleanup_expired_assets(self):
        """Cleanup expired audio files and transcripts."""
        db = SessionLocal()
        try:
            from app.db.models.conversation import ConversationTurn
            from datetime import timedelta
            
            # Delete audio files older than 30 days
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            
            old_turns = db.query(ConversationTurn).filter(
                ConversationTurn.created_at < cutoff_date
            ).all()
            
            for turn in old_turns:
                # TODO: Delete actual audio files from storage
                # if turn.audio_url:
                #     delete_file_from_storage(turn.audio_url)
                # if turn.tts_audio_url:
                #     delete_file_from_storage(turn.tts_audio_url)
                
                # Clear URLs (keep the record)
                turn.audio_url = None
                turn.tts_audio_url = None
            
            db.commit()
        finally:
            db.close()
    
    def _schedule_ivr_call(self, db: Session, patient_id: int):
        """Schedule IVR call for patient."""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return
        
        # Create scheduled call
        scheduled_call = ScheduledCall(
            patient_id=patient_id,
            scheduled_time=datetime.utcnow(),
            status=CallStatus.SCHEDULED,
            channel="ivr"
        )
        db.add(scheduled_call)
        db.commit()
        
        # Initiate call immediately
        self.call_service.initiate_call(patient, scheduled_call)
    
    def _send_sms_content(self, db: Session, patient_id: int):
        """Send SMS content to patient."""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return
        
        # Create session
        session = ConversationSession(
            patient_id=patient_id,
            channel="sms",
            status=SessionStatus.ACTIVE,
            started_at=datetime.utcnow()
        )
        db.add(session)
        db.commit()
        
        # Get patient's next lesson (TODO: implement lesson selection logic)
        # For now, send a generic message
        sms_flow = SMSFlow(session, db)
        # sms_flow.send_lesson_snippet(lesson_id)
    
    def _send_whatsapp_content(self, db: Session, patient_id: int):
        """Send WhatsApp content to patient."""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return
        
        # Create session
        session = ConversationSession(
            patient_id=patient_id,
            channel="whatsapp",
            status=SessionStatus.ACTIVE,
            started_at=datetime.utcnow()
        )
        db.add(session)
        db.commit()
        
        whatsapp_flow = WhatsAppFlow(session, db)
        # whatsapp_flow.send_lesson_content(lesson_id)
    
    def shutdown(self):
        """Shutdown scheduler."""
        self.scheduler.shutdown()
