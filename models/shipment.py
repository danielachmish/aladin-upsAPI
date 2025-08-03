from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from datetime import datetime
from database.session import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    track_no = Column(String, unique=True, index=True)
    customer_id = Column(String, index=True)
    invoice_number = Column(String)
    
    # Basic status fields
    status_code = Column(Integer)
    status_desc = Column(String)
    exception_code = Column(String, nullable=True)
    exception_desc = Column(String, nullable=True)
    
    # Delivery information
    estimated_delivery = Column(String, nullable=True)
    delivered_time = Column(String, nullable=True)
    received_by = Column(String, nullable=True)
    
    # UPS API additional fields that are commonly used
    service_code = Column(String, nullable=True)  # שירות UPS (Next Day, Ground וכו')
    package_weight = Column(Float, nullable=True)  # משקל החבילה
    package_dimensions = Column(String, nullable=True)  # מידות החבילה
    shipper_name = Column(String, nullable=True)  # שם השולח
    shipper_address = Column(Text, nullable=True)  # כתובת השולח
    recipient_name = Column(String, nullable=True)  # שם המקבל
    recipient_address = Column(Text, nullable=True)  # כתובת המקבל
    
    # Location tracking
    current_location = Column(String, nullable=True)  # מיקום נוכחי
    last_scan_location = Column(String, nullable=True)  # מיקום סריקה אחרון
    last_scan_time = Column(DateTime, nullable=True)  # זמן סריקה אחרון
    
    # Delivery attempt information
    delivery_attempt_count = Column(Integer, default=0)  # מספר ניסיונות מסירה
    delivery_instructions = Column(Text, nullable=True)  # הוראות מסירה
    signature_required = Column(Boolean, default=False)  # נדרשת חתימה
    
    # Reference fields (UPS supports multiple references)
    ref1 = Column(String, nullable=True)  # הפניה 1
    ref2 = Column(String, nullable=True)  # הפניה 2
    ref3 = Column(String, nullable=True)  # הפניה 3
    
    # Cost information
    shipping_cost = Column(Float, nullable=True)  # עלות משלוח
    insurance_value = Column(Float, nullable=True)  # ערך ביטוח
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<Shipment(track_no='{self.track_no}', status='{self.status_desc}')>"
