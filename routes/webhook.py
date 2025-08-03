from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.shipment import Shipment
from datetime import datetime

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Webhook: קבלת משלוחים מ-UPS
@router.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    now = datetime.utcnow()
    track_no = data.get("trackNo")

    shipment = db.query(Shipment).filter_by(track_no=track_no).first()

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

    db.commit()
    return {"message": "Shipment saved or updated successfully"}

# שליפת משלוחים ללקוח לפי ref1
@router.get("/shipments/{customer_id}")
def get_shipments_by_customer(customer_id: str, db: Session = Depends(get_db)):
    shipments = db.query(Shipment).filter(Shipment.customer_id == customer_id).all()

    return [
        {
            "track_no": s.track_no,
            "invoice_number": s.invoice_number,
            "status": s.status_desc,
            "delivered_time": s.delivered_time,
            "received_by": s.received_by
        } for s in shipments
    ]
