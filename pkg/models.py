from sqlalchemy import false
from pkg import Base, Column, Integer, String, Float, Boolean, ForeignKey, engine, relationship, Table, MetaData, Text, Date, Time, DateTime, func, text
from datetime import datetime


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    flow = Column(Text)
    updated_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())
    
    advertible_supplier = relationship('Advertible', back_populates='supplier_advertible', lazy=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)
class Advertible(Base):
    __tablename__ = 'advertible'

    id = Column(Integer, primary_key=True)
    adroll_id = Column(String(100))
    name = Column(String(100))
    status = Column(Integer)
    type_add = Column(String(100))

    organization_id = Column(Integer, ForeignKey('organization.id'), nullable=False)

    supplier_id = Column(Integer, ForeignKey('supplier.id'), nullable=True)
    supplier_advertible = relationship("Supplier", back_populates="advertible_supplier")

    
    campaigns_advertible = relationship('Campaigns', back_populates='advertible_campaigns', lazy=True)
    events_advertible = relationship('Events', back_populates='advertible_events', lazy=True)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())    

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return f"{str(self.name)} {str(self.adroll_id)}"

class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    rut = Column(Integer)
    dv = Column(Integer)
    b2b = Column(Boolean, unique=False, default=False)
    b2c = Column(Boolean, unique=False, default=False)
    profile_maker = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    advertibles = relationship('Advertible', backref='organization', lazy=True)

    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)


class Campaigns(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    provider_id = Column(String(255), unique=True)
    updated_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())

    advertisable_id = Column(Integer, ForeignKey('advertible.id'))
    advertible_campaigns = relationship("Advertible", back_populates="campaigns_advertible")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)

class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    provider_id = Column(String(255), unique=True)
    updated_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())

    advertisable_id = Column(Integer, ForeignKey('advertible.id'))
    advertible_events = relationship("Advertible", back_populates="events_advertible")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)