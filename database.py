from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

#DATABASE_URL = "mysql+pymysql://root:root@localhost:3307/benchmark_db"

DB_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_URL = f"mysql+pymysql://root:root@{DB_HOST}:3307/benchmark_db"



engine = create_engine(DATABASE_URL, echo=False)  # echo=False für weniger Output
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TestSession(Base):
    __tablename__ = "test_sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    server = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    num_requests = Column(Integer, nullable=False)
    started_at = Column(DateTime, default=datetime.now, nullable=False)
    finished_at = Column(DateTime, nullable=True)

    benchmark_overview = relationship("BenchmarkOverview", back_populates="test_session", cascade="all, delete-orphan")
    hardware_info = relationship("HardwareInfo", back_populates="test_session", uselist=False, cascade="all, delete-orphan")
    statistiken = relationship("Statistiken", back_populates="test_session", uselist=False, cascade="all, delete-orphan")


class BenchmarkOverview(Base):
    __tablename__ = "benchmark_overview"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    duration_ms = Column(Float, nullable=False)
    success_status = Column(Boolean, nullable=False)
    status = Column(Integer, nullable=False)
    request_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    test_session = relationship("TestSession", back_populates="benchmark_overview")


class HardwareInfo(Base):
    __tablename__ = "hardware_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    cpu_time_used = Column(Float, nullable=False)
    duration_ms = Column(Float, nullable=False)
    cpu_percent = Column(Float, nullable=False)
    memory_used_mb = Column(Float, nullable=False)
    memory_diff_mb = Column(Float, nullable=False)
    memory_vms_mb = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    test_session = relationship("TestSession", back_populates="hardware_info")


class Statistiken(Base):
    __tablename__ = "statistiken"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    avg_response_time = Column(Float, nullable=False)
    min_response_time = Column(Float, nullable=False)
    max_response_time = Column(Float, nullable=False)
    avg_error_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    test_session = relationship("TestSession", back_populates="statistiken")


def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Datenbank erstellt!")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()