from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.session import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    track_no = Column(String, unique=True, index=True)
    customer_id = Column(String, index=True)
    invoice_number = Column(String)
    status_code = Column(Integer)
    status_desc = Column(String)
    exception_code = Column(String, nullable=True)
    exception_desc = Column(String, nullable=True)
    estimated_delivery = Column(String, nullable=True)
    delivered_time = Column(String, nullable=True)
    received_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<Shipment(track_no='{self.track_no}', status='{self.status_desc}')>"
