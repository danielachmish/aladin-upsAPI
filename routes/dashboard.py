from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

from database.session import get_db
from models.shipment import Shipment

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

@router.get("/")
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        logger.info("Loading dashboard...")
        
        # Test database connection with retry
        retry_count = 3
        for attempt in range(retry_count):
            try:
                await db.execute(select(1))
                logger.info("Database connection test successful")
                break
            except Exception as e:
                logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
                if attempt == retry_count - 1:
                    logger.error(f"All database connection attempts failed")
                    return templates.TemplateResponse("dashboard.html", {
                        "request": request, 
                        "shipments": [],
                        "error": f"Database connection failed after {retry_count} attempts: {str(e)}"
                    })
                # Wait a bit before retry
                import asyncio
                await asyncio.sleep(0.5)
        
        # Try to get shipments with multiple fallback queries
        shipments = []
        
        # Try complex query first
        try:
            result = await db.execute(
                select(Shipment)
                .order_by(
                    Shipment.updated_at.desc().nulls_last(), 
                    Shipment.created_at.desc().nulls_last(),
                    Shipment.id.desc()
                )
                .limit(50)
            )
            shipments = result.scalars().all()
            logger.info("Complex query succeeded")
        except Exception as e:
            logger.warning(f"Complex query failed: {e}")
            
            # Try simple query
            try:
                result = await db.execute(select(Shipment).order_by(Shipment.id.desc()).limit(50))
                shipments = result.scalars().all()
                logger.info("Simple query succeeded")
            except Exception as e2:
                logger.warning(f"Simple query failed: {e2}")
                
                # Try most basic query
                try:
                    result = await db.execute(select(Shipment))
                    shipments = result.scalars().all()
                    logger.info("Basic query succeeded")
                except Exception as e3:
                    logger.error(f"All queries failed: {e3}")
                    return templates.TemplateResponse("dashboard.html", {
                        "request": request, 
                        "shipments": [],
                        "error": f"Query failed: {str(e3)}"
                    })
        
        logger.info(f"Found {len(shipments)} shipments")
        
        # Log some sample data
        if shipments:
            logger.info(f"Sample shipment: {shipments[0].track_no}")
            for i, ship in enumerate(shipments[:3]):
                logger.info(f"Shipment {i+1}: {ship.track_no} - {ship.status_desc}")
        else:
            logger.warning("No shipments found in database")
            
        return templates.TemplateResponse("dashboard.html", {"request": request, "shipments": shipments})
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return templates.TemplateResponse("dashboard.html", {
            "request": request, 
            "shipments": [],
            "error": f"Dashboard error: {str(e)}"
        })

@router.get("/debug/db-status")
async def db_status(db: AsyncSession = Depends(get_db)):
    try:
        # Simple count and select all
        result = await db.execute(select(Shipment))
        all_shipments = result.scalars().all()
        count = len(all_shipments)
        
        # Get sample data with more details
        sample_data = []
        if all_shipments:
            for shipment in all_shipments[:10]:  # First 10
                sample_data.append({
                    "id": shipment.id,
                    "track_no": shipment.track_no,
                    "customer_id": shipment.customer_id,
                    "status_desc": shipment.status_desc,
                    "created_at": str(shipment.created_at) if shipment.created_at else None,
                    "updated_at": str(shipment.updated_at) if shipment.updated_at else None
                })
        
        return {
            "database_connection": "OK",
            "total_shipments": count,
            "sample_data": sample_data,
            "note": "All data directly from the Render database"
        }
    except Exception as e:
        return {
            "database_connection": "ERROR",
            "error": str(e),
            "total_shipments": 0
        }

@router.get("/debug/add-test-data")
async def add_test_data_route(db: AsyncSession = Depends(get_db)):
    """Add test data directly to Render database"""
    try:
        # Check if test data already exists
        existing = await db.execute(select(Shipment).where(Shipment.track_no == "1Z999AA1234567890"))
        if existing.scalar():
            return {"message": "Test data already exists"}
        
        from datetime import datetime
        
        # Create test shipments
        test_shipments = [
            Shipment(
                track_no="1Z999AA1234567890",
                customer_id="CUST001",
                invoice_number="INV001",
                status_code=10,
                status_desc="In Transit",
                estimated_delivery="2025-08-05",
                created_at=datetime.now()
            ),
            Shipment(
                track_no="1Z999BB9876543210",
                customer_id="CUST002",
                invoice_number="INV002", 
                status_code=20,
                status_desc="Delivered",
                delivered_time="2025-08-03 14:30:00",
                received_by="John Doe",
                created_at=datetime.now()
            ),
            Shipment(
                track_no="1Z999CC1122334455",
                customer_id="CUST003",
                invoice_number="INV003",
                status_code=5,
                status_desc="Processing",
                estimated_delivery="2025-08-06",
                created_at=datetime.now()
            )
        ]
        
        for shipment in test_shipments:
            db.add(shipment)
        
        await db.commit()
        
        return {
            "message": f"Added {len(test_shipments)} test shipments to database",
            "shipments": [s.track_no for s in test_shipments]
        }
    except Exception as e:
        await db.rollback()
        return {
            "error": str(e),
            "message": "Failed to add test data"
        }
