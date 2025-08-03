from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.session import engine, Base
# Import models BEFORE creating tables so they register with Base
from models.shipment import Shipment
from routes.webhook import router as webhook_router
from routes.dashboard import router as dashboard_router
from routes.api import router as api_router


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
app.include_router(api_router)

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

# Simple test route
@app.get("/simple-test")
async def simple_test():
    try:
        from database.session import AsyncSessionLocal
        from sqlalchemy.future import select
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Shipment))
            shipments = result.scalars().all()
            return {
                "total_shipments": len(shipments),
                "shipment_data": [
                    {
                        "track_no": s.track_no,
                        "customer_id": s.customer_id,
                        "status_desc": s.status_desc
                    } for s in shipments[:3]  # First 3
                ]
            }
    except Exception as e:
        return {"error": str(e)}
