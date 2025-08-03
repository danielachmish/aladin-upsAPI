from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.session import engine, Base
# Import models BEFORE creating tables so they register with Base
from models.shipment import Shipment
from routes.webhook import router as webhook_router
from routes.dashboard import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    try:
        print("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
    yield

app = FastAPI(title="UPS Tracker", lifespan=lifespan)

# ראוטרים
app.include_router(webhook_router)
app.include_router(dashboard_router)

# Test database connection
@app.get("/test-db")
async def test_database():
    """Test database connection and show raw data"""
    try:
        from database.session import AsyncSessionLocal
        from sqlalchemy import text
        
        async with AsyncSessionLocal() as session:
            # Test connection
            result = await session.execute(text("SELECT 1"))
            connection_test = result.scalar()
            
            # Check if table exists
            table_check = await session.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'shipments')"))
            table_exists = table_check.scalar()
            
            # Count rows
            if table_exists:
                count_result = await session.execute(text("SELECT COUNT(*) FROM shipments"))
                row_count = count_result.scalar()
                
                # Get sample data
                sample_result = await session.execute(text("SELECT * FROM shipments LIMIT 3"))
                sample_data = [dict(row._mapping) for row in sample_result]
            else:
                row_count = 0
                sample_data = []
            
            return {
                "connection_test": connection_test,
                "table_exists": table_exists,
                "row_count": row_count,
                "sample_data": sample_data,
                "status": "OK"
            }
    except Exception as e:
        return {
            "error": str(e),
            "status": "ERROR"
        }

# סטטוס API
@app.get("/status")
def root():
    return {"status": "UPS Tracker API is live!"}
