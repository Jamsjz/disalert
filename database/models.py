from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///sqlite.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    alerts = relationship("Alert", back_populates="user")


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_type = Column(String, nullable=False)
    creation_times = relationship("AlertTime", back_populates="alert")
    location = relationship("Location", back_populates="alerts")
    user = relationship("User", back_populates="alerts")


class AlertTime(Base):
    __tablename__ = "alert_times"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    alert = relationship("Alert", back_populates="creation_times")


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    road = Column(String)
    alerts = relationship("Alert", back_populates="location")


Base.metadata.create_all(engine)
