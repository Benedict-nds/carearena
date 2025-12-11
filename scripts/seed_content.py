"""Script to seed initial content."""

from app.db.database import SessionLocal
from app.services.content_service import ContentService
from app.schemas.content import ConditionCreate


def seed_content():
    """Seed initial content data."""
    db = SessionLocal()
    try:
        content_service = ContentService()
        
        # Create sample conditions
        conditions_data = [
            {"name": "Diabetes", "description": "Diabetes management and education"},
            {"name": "Hypertension", "description": "High blood pressure management"},
            {"name": "Heart Disease", "description": "Cardiac care education"},
        ]
        
        for condition_data in conditions_data:
            condition_create = ConditionCreate(**condition_data)
            condition = content_service.create_condition(db, condition_create)
            print(f"Created condition: {condition.name}")
        
        print("Content seeding completed")
    finally:
        db.close()


if __name__ == "__main__":
    seed_content()

