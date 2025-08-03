"""
Script to add test data to the database
"""
import asyncio
from database.session import AsyncSessionLocal
from models.shipment import Shipment
from datetime import datetime

async def add_test_data():
    async with AsyncSessionLocal() as session:
        # Create test shipments
        test_shipments = [
            Shipment(
                track_no="1Z999AA1234567890",
                customer_id="CUST001",
                invoice_number="INV001",
                status_code=10,
                status_desc="In Transit",
                estimated_delivery="2025-08-05",
                created_at=datetime.now()
            ),
            Shipment(
                track_no="1Z999BB9876543210",
                customer_id="CUST002",
                invoice_number="INV002", 
                status_code=20,
                status_desc="Delivered",
                delivered_time="2025-08-03 14:30:00",
                received_by="John Doe",
                created_at=datetime.now()
            ),
            Shipment(
                track_no="1Z999CC1122334455",
                customer_id="CUST003",
                invoice_number="INV003",
                status_code=5,
                status_desc="Processing",
                estimated_delivery="2025-08-06",
                created_at=datetime.now()
            )
        ]
        
        for shipment in test_shipments:
            session.add(shipment)
        
        await session.commit()
        print(f"Added {len(test_shipments)} test shipments to database")

if __name__ == "__main__":
    asyncio.run(add_test_data())
