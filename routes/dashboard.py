from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models.shipment import Shipment

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
def dashboard_view(request: Request, db: Session = Depends(get_db)):
    shipments = db.query(Shipment).order_by(Shipment.updated_at.desc()).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "shipments": shipments})
