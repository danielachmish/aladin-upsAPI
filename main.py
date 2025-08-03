from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes.webhook import router as webhook_router
from routes.dashboard import router as dashboard_router
from database.session import engine
from models.shipment import Shipment


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    try:
        from database.session import Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Warning: Could not create tables: {e}")
    yield

app = FastAPI(title="UPS Tracker", lifespan=lifespan)

# ראוטרים
app.include_router(webhook_router)
app.include_router(dashboard_router)

# סטטוס API
@app.get("/status")
def root():
    return {"status": "UPS Tracker API is live!"}
