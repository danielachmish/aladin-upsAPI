from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    track_no = Column(String, unique=True, index=True)
    customer_id = Column(String, index=True)  # ref1
    invoice_number = Column(String)  # ref2
    status_code = Column(Integer)
    status_desc = Column(String)
    exception_code = Column(String, nullable=True)
    exception_desc = Column(String, nullable=True)
    estimated_delivery = Column(String, nullable=True)
    delivered_time = Column(String, nullable=True)
    received_by = Column(String, nullable=True)
    updated_at = Column(DateTime)
