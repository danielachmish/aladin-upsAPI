import asyncio
from database.session import AsyncSessionLocal
from sqlalchemy import text

async def check_table_structure():
    async with AsyncSessionLocal() as session:
        # בדיקת עמודות קיימות
        result = await session.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'shipments' 
            ORDER BY ordinal_position
        """))
        columns = result.fetchall()
        print('עמודות קיימות בטבלה:')
        for col in columns:
            print(f'  {col[0]} - {col[1]} ({"NULL" if col[2] == "YES" else "NOT NULL"})')

if __name__ == "__main__":
    asyncio.run(check_table_structure())
