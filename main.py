from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from routes.webhook import router as webhook_router

from routes.dashboard import router as dashboard_router
from fastapi.staticfiles import StaticFiles
from routes.dashboard import router as dashboard_router

DATABASE_URL = "postgresql+asyncpg://user:password@host:port/dbname"  # החלף בהתאם

app = FastAPI(title="UPS Tracker")
app.include_router(webhook_router)

templates = Jinja2Templates(directory="templates")

# חיבור למסד נתונים
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@app.get("/")
async def dashboard(request: Request):
    async with AsyncSessionLocal() as session:
        logs = (await session.execute(Log.__table__.select().order_by(Log.timestamp.desc()).limit(20))).fetchall()
        tracking = (await session.execute(TrackingData.__table__.select().limit(20))).fetchall()
    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs, "tracking": tracking})

app.include_router(dashboard_router)


app.include_router(dashboard_router)
app.mount("/static", StaticFiles(directory="static"), name="static")  # אם תוסיף CSS בעתיד

@app.get("/")
def root():
    return {"status": "UPS Tracker API is live!"}
