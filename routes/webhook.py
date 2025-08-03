from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from database.session import get_db
from models.shipment import Shipment

router = APIRouter()

@router.post("/webhook")
async def receive_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    now = datetime.utcnow()
    track_no = data.get("trackNo")

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
            updated_at=now,
        )
        db.add(shipment)

    await db.commit()
    return {"message": "Shipment saved or updated successfully"}
