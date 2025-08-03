"""
Migration script to add UPS API fields to shipments table
"""
import asyncio
from database.session import AsyncSessionLocal
from sqlalchemy import text

async def migrate_table():
    async with AsyncSessionLocal() as session:
        try:
            print("מתחיל הוספת עמודות חדשות לטבלת shipments...")
            
            # רשימת עמודות חדשות להוספה
            new_columns = [
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS service_code VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS package_weight FLOAT",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS package_dimensions VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS shipper_name VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS shipper_address TEXT",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS recipient_name VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS recipient_address TEXT",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS current_location VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS last_scan_location VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS last_scan_time TIMESTAMP",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS delivery_attempt_count INTEGER DEFAULT 0",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS delivery_instructions TEXT",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS signature_required BOOLEAN DEFAULT FALSE",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS ref1 VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS ref2 VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS ref3 VARCHAR",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS shipping_cost FLOAT",
                "ALTER TABLE shipments ADD COLUMN IF NOT EXISTS insurance_value FLOAT"
            ]
            
            for i, sql in enumerate(new_columns, 1):
                print(f"מוסיף עמודה {i}/{len(new_columns)}...")
                await session.execute(text(sql))
                await session.commit()
                print(f"✓ הוספת עמודה {i} הושלמה")
            
            print("\n🎉 כל העמודות החדשות נוספו בהצלחה!")
            
            # בדיקת התוצאה
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'shipments' 
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            print(f"\nסה\"כ עמודות בטבלה כעת: {len(columns)}")
            print("עמודות חדשות שנוספו:")
            expected_new_columns = [
                'service_code', 'package_weight', 'package_dimensions', 
                'shipper_name', 'shipper_address', 'recipient_name', 
                'recipient_address', 'current_location', 'last_scan_location', 
                'last_scan_time', 'delivery_attempt_count', 'delivery_instructions', 
                'signature_required', 'ref1', 'ref2', 'ref3', 
                'shipping_cost', 'insurance_value'
            ]
            
            existing_columns = [col[0] for col in columns]
            for new_col in expected_new_columns:
                if new_col in existing_columns:
                    print(f"  ✓ {new_col}")
                else:
                    print(f"  ✗ {new_col} - לא נמצא!")
                    
        except Exception as e:
            print(f"❌ שגיאה במהלך המיגרציה: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(migrate_table())
