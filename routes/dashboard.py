from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.session import get_db
from models.shipment import Shipment

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Shipment).order_by(Shipment.updated_at.desc()).limit(50))
    shipments = result.scalars().all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "shipments": shipments})
