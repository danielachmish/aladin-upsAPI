from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from routes.webhook import router as webhook_router
from routes.dashboard import router as dashboard_router
from models.shipment import Shipment  


DATABASE_URL = "postgresql+asyncpg://postgres:020796@localhost:5432/postgres"

app = FastAPI(title="UPS Tracker")

# חיבור למסד הנתונים
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# תבניות
templates = Jinja2Templates(directory="templates")

# ראוטרים
app.include_router(webhook_router)
app.include_router(dashboard_router)

# קבצים סטטיים


# דשבורד
@app.get("/")
async def dashboard(request: Request):
    async with AsyncSessionLocal() as session:
        shipments = (await session.execute(Shipment.__table__.select().limit(20))).fetchall()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "shipments": shipments  # השם כאן חייב להתאים ל־HTML
    })

# סטטוס API
@app.get("/status")
def root():
    return {"status": "UPS Tracker API is live!"}
