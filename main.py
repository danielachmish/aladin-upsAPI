from fastapi import FastAPI

from routes.webhook import router as webhook_router
from routes.dashboard import router as dashboard_router

app = FastAPI(title="UPS Tracker")

# ראוטרים
app.include_router(webhook_router)
app.include_router(dashboard_router)

# סטטוס API
@app.get("/status")
def root():
    return {"status": "UPS Tracker API is live!"}
