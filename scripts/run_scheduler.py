"""Script to run the scheduler service."""

import asyncio
from datetime import datetime
from app.db.database import SessionLocal
from app.services.scheduler_service import SchedulerService
from app.services.call_service import CallService


def run_scheduler():
    """Run scheduler to process upcoming calls."""
    db = SessionLocal()
    try:
        scheduler_service = SchedulerService()
        upcoming_calls = scheduler_service.get_upcoming_calls(db)
        
        for call in upcoming_calls:
            # Check if it's time to make the call
            if call.scheduled_time <= datetime.utcnow():
                # Initiate call
                call_service = CallService()
                result = call_service.initiate_call(call.patient, call)
                
                # Update call status
                call.status = "in_progress"
                db.commit()
                
                print(f"Initiated call for patient {call.patient_id}: {result}")
    finally:
        db.close()


if __name__ == "__main__":
    run_scheduler()

