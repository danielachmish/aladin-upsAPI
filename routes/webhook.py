from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import logging

from database.session import get_db
from models.shipment import Shipment

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def receive_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        data = await request.json()
        logger.info(f"Received webhook data: {data}")
        
        now = datetime.utcnow()
        track_no = data.get("trackNo")
        
        if not track_no:
            raise HTTPException(status_code=400, detail="trackNo is required")

        result = await db.execute(select(Shipment).where(Shipment.track_no == track_no))
        shipment = result.scalars().first()

        if shipment:
            shipment.status_code = int(data.get("statusCode", 0))
            shipment.status_desc = data.get("statusDescHeb")
            shipment.exception_code = data.get("exceptionCode")
            shipment.exception_desc = data.get("exceptionDescHeb")
            shipment.estimated_delivery = data.get("estimateDelivery")
            shipment.delivered_time = data.get("deliveredTime")
            shipment.received_by = data.get("receivedBy")
            shipment.updated_at = now
            logger.info(f"Updated existing shipment: {track_no}")
        else:
            shipment = Shipment(
                track_no=track_no,
                customer_id=data.get("ref1"),
                invoice_number=data.get("ref2"),
                status_code=int(data.get("statusCode", 0)),
                status_desc=data.get("statusDescHeb"),
                exception_code=data.get("exceptionCode"),
                exception_desc=data.get("exceptionDescHeb"),
                estimated_delivery=data.get("estimateDelivery"),
                delivered_time=data.get("deliveredTime"),
                received_by=data.get("receivedBy"),
                created_at=now,
                updated_at=now,
            )
            db.add(shipment)
            logger.info(f"Created new shipment: {track_no}")

        await db.commit()
        return {"message": "Shipment saved or updated successfully", "track_no": track_no}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/test-webhook")
async def test_webhook(db: AsyncSession = Depends(get_db)):
    """Test endpoint to create a sample shipment"""
    try:
        test_data = {
            "trackNo": "TEST123456",
            "ref1": "CUSTOMER001",
            "ref2": "INV001",
            "statusCode": "5",
            "statusDescHeb": "במעבר",
            "exceptionCode": None,
            "exceptionDescHeb": None,
            "estimateDelivery": "2025-08-05",
            "deliveredTime": None,
            "receivedBy": None
        }
        
        now = datetime.utcnow()
        
        # Check if exists
        result = await db.execute(select(Shipment).where(Shipment.track_no == test_data["trackNo"]))
        existing = result.scalars().first()
        
        if existing:
            return {"message": "Test shipment already exists", "track_no": test_data["trackNo"]}
        
        # Create new
        shipment = Shipment(
            track_no=test_data["trackNo"],
            customer_id=test_data["ref1"],
            invoice_number=test_data["ref2"],
            status_code=int(test_data["statusCode"]),
            status_desc=test_data["statusDescHeb"],
            exception_code=test_data.get("exceptionCode"),
            exception_desc=test_data.get("exceptionDescHeb"),
            estimated_delivery=test_data.get("estimateDelivery"),
            delivered_time=test_data.get("deliveredTime"),
            received_by=test_data.get("receivedBy"),
            created_at=now,
            updated_at=now,
        )
        db.add(shipment)
        await db.commit()
        
        return {"message": "Test shipment created successfully", "track_no": test_data["trackNo"]}
    
    except Exception as e:
        logger.error(f"Error creating test shipment: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
