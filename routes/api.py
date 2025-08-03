from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
import logging
from typing import List, Optional

from database.session import get_db
from models.shipment import Shipment

router = APIRouter(prefix="/api/v1")
logger = logging.getLogger(__name__)

@router.get("/shipments/customer/{customer_id}")
async def get_customer_shipments(
    customer_id: str,
    db: AsyncSession = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, le=100, description="Maximum number of results")
):
    """
    קבלת משלוחים לפי מזהה לקוח - לשימוש WordPress
    """
    try:
        query = select(Shipment).where(Shipment.customer_id == customer_id)
        
        if status:
            query = query.where(Shipment.status_desc.ilike(f"%{status}%"))
        
        query = query.order_by(Shipment.updated_at.desc().nulls_last()).limit(limit)
        
        result = await db.execute(query)
        shipments = result.scalars().all()
        
        return {
            "customer_id": customer_id,
            "total_shipments": len(shipments),
            "shipments": [
                {
                    "track_no": s.track_no,
                    "invoice_number": s.invoice_number,
                    "status_code": s.status_code,
                    "status_desc": s.status_desc,
                    "exception_code": s.exception_code,
                    "exception_desc": s.exception_desc,
                    "estimated_delivery": s.estimated_delivery,
                    "delivered_time": s.delivered_time,
                    "received_by": s.received_by,
                    "current_location": s.current_location,
                    "last_scan_location": s.last_scan_location,
                    "delivery_attempt_count": s.delivery_attempt_count,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                    "updated_at": s.updated_at.isoformat() if s.updated_at else None
                }
                for s in shipments
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching shipments for customer {customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/shipments/track/{track_no}")
async def get_shipment_by_tracking(
    track_no: str,
    db: AsyncSession = Depends(get_db)
):
    """
    חיפוש משלוח לפי מספר מעקב
    """
    try:
        result = await db.execute(select(Shipment).where(Shipment.track_no == track_no))
        shipment = result.scalars().first()
        
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        return {
            "track_no": shipment.track_no,
            "customer_id": shipment.customer_id,
            "invoice_number": shipment.invoice_number,
            "status_code": shipment.status_code,
            "status_desc": shipment.status_desc,
            "exception_code": shipment.exception_code,
            "exception_desc": shipment.exception_desc,
            "estimated_delivery": shipment.estimated_delivery,
            "delivered_time": shipment.delivered_time,
            "received_by": shipment.received_by,
            "service_code": shipment.service_code,
            "current_location": shipment.current_location,
            "last_scan_location": shipment.last_scan_location,
            "delivery_attempt_count": shipment.delivery_attempt_count,
            "created_at": shipment.created_at.isoformat() if shipment.created_at else None,
            "updated_at": shipment.updated_at.isoformat() if shipment.updated_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching shipment {track_no}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """
    בדיקת תקינות API
    """
    return {
        "status": "healthy",
        "message": "UPS Tracker API is running",
        "endpoints": {
            "customer_shipments": "/api/v1/shipments/customer/{customer_id}",
            "track_shipment": "/api/v1/shipments/track/{track_no}",
            "webhook": "/webhook"
        }
    }
