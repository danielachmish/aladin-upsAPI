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
        result = await db.execute(select(Shipment).order_by(Shipment.updated_at.desc()).limit(50))
        shipments = result.scalars().all()
        logger.info(f"Found {len(shipments)} shipments")
        
        # Log some sample data
        if shipments:
            logger.info(f"Sample shipment: {shipments[0].track_no}")
        else:
            logger.warning("No shipments found in database")
            
        return templates.TemplateResponse("dashboard.html", {"request": request, "shipments": shipments})
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return templates.TemplateResponse("dashboard.html", {"request": request, "shipments": []})

@router.get("/debug/db-status")
async def db_status(db: AsyncSession = Depends(get_db)):
    try:
        # Count total shipments
        count_result = await db.execute(select(Shipment))
        all_shipments = count_result.scalars().all()
        count = len(all_shipments)
        
        # Get sample data
        sample_data = []
        if all_shipments:
            for shipment in all_shipments[:3]:  # First 3
                sample_data.append({
                    "track_no": shipment.track_no,
                    "status_desc": shipment.status_desc,
                    "updated_at": str(shipment.updated_at) if shipment.updated_at else None
                })
        
        return {
            "database_connection": "OK",
            "total_shipments": count,
            "sample_data": sample_data
        }
    except Exception as e:
        return {
            "database_connection": "ERROR",
            "error": str(e),
            "total_shipments": 0
        }
