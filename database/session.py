import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:020796@localhost/postgres")

# Fix DATABASE_URL for async if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

print(f"Database URL (masked): {DATABASE_URL.split('@')[0]}@***")  # Log for debugging

# Create Base FIRST
Base = declarative_base()

try:
    engine = create_async_engine(
        DATABASE_URL, 
        echo=True,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        pool_size=5,         # Number of connections to maintain
        max_overflow=10      # Additional connections if needed
    )
    print("Database engine created successfully")
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            # Test connection before yielding
            await session.execute(text("SELECT 1"))
            yield session
        except Exception as e:
            print(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
