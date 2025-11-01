from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    created_at = Column(Date, default=date.today)

    applications = relationship("Application", back_populates="user")
    subscription = relationship("Subscription", uselist=False, back_populates="user")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_order_number = Column(String, nullable=True)
    title = Column(String)
    employer = Column(String)
    location = Column(String)      # Ex: "Fresno, CA"
    state = Column(String)         # Ex: "CA"
    visa_type = Column(String)     # "H-2A" ou "H-2B"
    description = Column(String)
    contact_email = Column(String)
    posted_at = Column(Date)
    expires_at = Column(Date)

    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    sent_at = Column(Date, default=date.today)
    status = Column(String, default="sent")  # "sent", "replied", "waiting"

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    status = Column(String, default="inactive")  # "active", "cancelled", etc.
    lemon_squeezy_subscription_id = Column(String, nullable=True)
    created_at = Column(Date, default=date.today)

    user = relationship("User", back_populates="subscription")
