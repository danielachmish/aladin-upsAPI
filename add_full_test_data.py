"""
Script to add comprehensive UPS test data with all new fields
"""
import asyncio
from database.session import AsyncSessionLocal
from models.shipment import Shipment
from datetime import datetime

async def add_full_ups_test_data():
    async with AsyncSessionLocal() as session:
        print("מוסיף נתוני בדיקה מלאים עם כל השדות החדשים...")
        
        # Create comprehensive test shipments
        test_shipments = [
            Shipment(
                track_no="1Z999UPS0001234567",
                customer_id="CUST_UPS_001",
                invoice_number="INV_UPS_001",
                status_code=10,
                status_desc="In Transit",
                estimated_delivery="2025-08-06",
                
                # UPS specific fields
                service_code="UPS_GROUND",
                package_weight=2.5,
                package_dimensions="30x20x15 cm",
                shipper_name="חברת ABC בע\"מ",
                shipper_address="רחוב הרצל 123, תל אביב, ישראל",
                recipient_name="יוסי כהן",
                recipient_address="רחוב בן יהודה 45, ירושלים, ישראל",
                current_location="מרכז הפצה תל אביב",
                last_scan_location="נמל התעופה בן גוריון",
                last_scan_time=datetime.now(),
                delivery_attempt_count=0,
                delivery_instructions="השאיר ליד הדלת",
                signature_required=True,
                ref1="CUST_UPS_001",
                ref2="ORDER_12345",
                ref3="PRIORITY",
                shipping_cost=45.50,
                insurance_value=500.00,
                created_at=datetime.now()
            ),
            
            Shipment(
                track_no="1Z999UPS0007654321",
                customer_id="CUST_UPS_002", 
                invoice_number="INV_UPS_002",
                status_code=20,
                status_desc="Delivered",
                delivered_time="2025-08-02 14:30:00",
                received_by="שרה לוי",
                
                # UPS specific fields
                service_code="UPS_NEXT_DAY",
                package_weight=1.2,
                package_dimensions="25x15x10 cm",
                shipper_name="חנות XYZ",
                shipper_address="שדרות יפו 200, ירושלים, ישראל",
                recipient_name="שרה לוי",
                recipient_address="רחוב ארלוזורוב 78, תל אביב, ישראל",
                current_location="נמסר ללקוח",
                last_scan_location="תל אביב - מרכז העיר",
                last_scan_time=datetime.now(),
                delivery_attempt_count=1,
                delivery_instructions="צלצל לפני מסירה",
                signature_required=True,
                ref1="CUST_UPS_002",
                ref2="ORDER_67890",
                ref3="EXPRESS",
                shipping_cost=89.90,
                insurance_value=1200.00,
                created_at=datetime.now()
            ),
            
            Shipment(
                track_no="1Z999UPS0005555555",
                customer_id="CUST_UPS_003",
                invoice_number="INV_UPS_003",
                status_code=90,
                status_desc="Exception - Address Correction",
                exception_code="DEL001",
                exception_desc="כתובת לא מדויקת - נדרש תיקון",
                estimated_delivery="2025-08-08",
                
                # UPS specific fields  
                service_code="UPS_2DAY",
                package_weight=5.8,
                package_dimensions="40x30x25 cm",
                shipper_name="מפעל הטכנולוגיה",
                shipper_address="אזור התעשייה, חיפה, ישראל",
                recipient_name="דוד אברהם",
                recipient_address="כתובת לא מדויקת - רחוב לא ידוע",
                current_location="ממתין לתיקון כתובת",
                last_scan_location="חיפה - מרכז הפצה",
                last_scan_time=datetime.now(),
                delivery_attempt_count=2,
                delivery_instructions="בדיקת כתובת נדרשת",
                signature_required=False,
                ref1="CUST_UPS_003",
                ref2="ORDER_11111",
                ref3="STANDARD",
                shipping_cost=65.00,
                insurance_value=800.00,
                created_at=datetime.now()
            ),
            
            Shipment(
                track_no="1Z999UPS0009999999",
                customer_id="CUST_UPS_004",
                invoice_number="INV_UPS_004", 
                status_code=15,
                status_desc="Out for Delivery",
                estimated_delivery="2025-08-03",
                
                # UPS specific fields
                service_code="UPS_GROUND",
                package_weight=3.2,
                package_dimensions="35x25x20 cm",
                shipper_name="אלקטרוניקה פלוס",
                shipper_address="רחוב אלנבי 150, תל אביב, ישראל",
                recipient_name="מיכל גרין",
                recipient_address="שכונת רמת גן, רחוב ביאליק 22",
                current_location="ברכב המשלוחים",
                last_scan_location="רמת גן - מרכז הפצה",
                last_scan_time=datetime.now(),
                delivery_attempt_count=0,
                delivery_instructions="מסירה בין 9:00-17:00",
                signature_required=True,
                ref1="CUST_UPS_004",
                ref2="ORDER_99999",
                ref3="NORMAL",
                shipping_cost=35.75,
                insurance_value=400.00,
                created_at=datetime.now()
            )
        ]
        
        for i, shipment in enumerate(test_shipments, 1):
            session.add(shipment)
            print(f"✓ נוסף משלוח {i}: {shipment.track_no} - {shipment.status_desc}")
        
        await session.commit()
        print(f"\n🎉 נוספו {len(test_shipments)} משלוחים מלאים עם כל שדות UPS!")
        print("כל השדות החדשים מכילים נתונים אמיתיים.")

if __name__ == "__main__":
    asyncio.run(add_full_ups_test_data())
