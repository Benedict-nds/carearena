"""CSV importer service."""

import csv
from typing import List, Dict
from sqlalchemy.orm import Session
from app.db.models.patient import Patient
from app.db.models.hospital import Hospital
from app.utils.phone_utils import normalize_phone_number


class CSVImporterService:
    """Service for importing hospital CSV data with deduplication."""
    
    @staticmethod
    def import_patients_from_csv(db: Session, hospital_id: int, csv_file_path: str) -> Dict[str, int]:
        """Import patients from CSV file with deduplication by phone number."""
        imported_count = 0
        skipped_count = 0
        error_count = 0
        errors = []
        
        # Expected CSV format: first_name, last_name, phone_number, date_of_birth, language_preference
        
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                try:
                    phone_number = row.get('phone_number', '').strip()
                    if not phone_number:
                        error_count += 1
                        errors.append({"row": row_num, "error": "Missing phone number"})
                        continue
                    
                    # Normalize phone number
                    normalized_phone = normalize_phone_number(phone_number)
                    if not normalized_phone:
                        error_count += 1
                        errors.append({"row": row_num, "error": "Invalid phone number format"})
                        continue
                    
                    # Check for duplicate phone number
                    existing_patient = db.query(Patient).filter(
                        Patient.phone_number == normalized_phone
                    ).first()
                    
                    if existing_patient:
                        skipped_count += 1
                        continue
                    
                    # Create new patient
                    patient = Patient(
                        hospital_id=hospital_id,
                        first_name=row.get('first_name', '').strip(),
                        last_name=row.get('last_name', '').strip(),
                        phone_number=normalized_phone,
                        language_preference=row.get('language_preference', 'en').strip() or 'en'
                    )
                    db.add(patient)
                    imported_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append({"row": row_num, "error": str(e)})
                    continue
        
        db.commit()
        
        return {
            "imported": imported_count,
            "skipped": skipped_count,
            "errors": error_count,
            "error_details": errors[:10]  # Limit error details
        }

