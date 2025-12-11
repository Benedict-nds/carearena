"""Manual CSV import script."""

import sys
from app.db.database import SessionLocal
from app.services.csv_importer import CSVImporterService


def import_csv(hospital_id: int, csv_file_path: str):
    """Import CSV file for a hospital."""
    db = SessionLocal()
    try:
        importer = CSVImporterService()
        result = importer.import_patients_from_csv(db, hospital_id, csv_file_path)
        print(f"Import completed: {result['imported']} imported, {result['errors']} errors")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python import_csv_manual.py <hospital_id> <csv_file_path>")
        sys.exit(1)
    
    hospital_id = int(sys.argv[1])
    csv_file_path = sys.argv[2]
    import_csv(hospital_id, csv_file_path)

