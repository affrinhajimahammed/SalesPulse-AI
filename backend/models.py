
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class Territory(Base):
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    region = Column(String, nullable=False)

    sales_reps = relationship("SalesRep", back_populates="territory")


class SalesRep(Base):
    __tablename__ = "sales_reps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    territory_id = Column(Integer, ForeignKey("territories.id"))

    territory = relationship("Territory", back_populates="sales_reps")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    industry = Column(String)
    territory_id = Column(Integer, ForeignKey("territories.id"))

    opportunities = relationship("Opportunity", back_populates="account")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    stage = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    expected_close_date = Column(DateTime)

    account_id = Column(Integer, ForeignKey("accounts.id"))
    sales_rep_id = Column(Integer, ForeignKey("sales_reps.id"))

    account = relationship("Account", back_populates="opportunities")

class StageHistory(Base):
    __tablename__ = "stage_history"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    old_stage = Column(String)
    new_stage = Column(String, nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    activity_type = Column(String, nullable=False)
    activity_date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)

class Quota(Base):
    __tablename__ = "quotas"

    id = Column(Integer, primary_key=True, index=True)
    sales_rep_id = Column(Integer, ForeignKey("sales_reps.id"))
    target_amount = Column(Float, nullable=False)
    period = Column(String, nullable=False)


class HistoricalBooking(Base):
    __tablename__ = "historical_bookings"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    booking_amount = Column(Float, nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)

class ForecastSnapshot(Base):
    __tablename__ = "forecast_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    forecast_date = Column(DateTime, default=datetime.utcnow)
    period = Column(String, nullable=False)
    total_pipeline = Column(Float, default=0.0)
    expected_revenue = Column(Float, default=0.0)
    best_case = Column(Float, default=0.0)
    worst_case = Column(Float, default=0.0)
