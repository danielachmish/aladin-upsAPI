from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from database.session import get_db
from models.shipment import Shipment

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

@router.get("/")
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        logger.info("Loading dashboard...")
        
        # Test database connection first
        try:
            await db.execute(select(1))
            logger.info("Database connection test successful")
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return templates.TemplateResponse("dashboard.html", {
                "request": request, 
                "shipments": [],
                "error": f"Database connection failed: {str(e)}"
            })
        
        # Try the complex query first
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
            logger.warning(f"Complex query failed, trying simple query: {e}")
            # Fallback to simple query
            try:
                result = await db.execute(select(Shipment).order_by(Shipment.id.desc()).limit(50))
                shipments = result.scalars().all()
                logger.info("Simple query succeeded")
            except Exception as e2:
                logger.error(f"Simple query also failed: {e2}")
                return templates.TemplateResponse("dashboard.html", {
                    "request": request, 
                    "shipments": [],
                    "error": f"Query failed: {str(e2)}"
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
            for shipment in all_shipments[:5]:  # First 5
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
            "note": "If you see data here but not on dashboard, there might be a query issue"
        }
    except Exception as e:
        return {
            "database_connection": "ERROR",
            "error": str(e),
            "total_shipments": 0
        }
