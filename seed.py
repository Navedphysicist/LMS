from db.database import engine, Base, get_db
from utils.seed_utils import seed_database
# Create all tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Seeding database...")
    db = next(get_db())
    seed_database(db)
    print("Database seeded successfully!")