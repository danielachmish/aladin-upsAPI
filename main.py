from fastapi import FastAPI
from routes.webhook import router as webhook_router

app = FastAPI(title="UPS Tracker")

app.include_router(webhook_router)
