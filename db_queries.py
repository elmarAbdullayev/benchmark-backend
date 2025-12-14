from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends

# Updated imports
from database import BenchmarkOverview, HardwareInfo, Statistiken
from database import get_db

query_api = APIRouter(prefix="/db", tags=["Database Queries"])


# -------------------------------
# Benchmark Overview (Eski: benchmark_results)
# -------------------------------
@query_api.get("/benchmark-overview")
async def get_all_benchmark_overview(db: Session = Depends(get_db)):
    """Holt alle Benchmark-Übersichtsdatensätze"""
    results = db.query(BenchmarkOverview).all()
    return results


# -------------------------------
# Hardware Info (Eski: hardware_results)
# -------------------------------
@query_api.get("/hardware-info")
async def get_all_hardware_info(db: Session = Depends(get_db)):
    """Holt alle Hardware-Informationen"""
    results = db.query(HardwareInfo).all()
    return results


# -------------------------------
# Statistiken (Eski: avg_results)
# -------------------------------
@query_api.get("/statistiken")
async def get_all_statistiken(db: Session = Depends(get_db)):
    """Holt alle Statistik-Datensätze"""
    results = db.query(Statistiken).all()
    return results


# -------------------------------
# Kombinierte Ergebnisse
# -------------------------------
@query_api.get("/combined-results")
async def get_combined_results(db: Session = Depends(get_db)):
    """
    Kombiniert Benchmark- und Hardware-Daten
    """

    # Benchmark Overview
    benchmark = db.query(
        BenchmarkOverview.duration_ms,
        BenchmarkOverview.success_status,
        BenchmarkOverview.status,
        BenchmarkOverview.request_id,
        BenchmarkOverview.created_at,
        BenchmarkOverview.test_session_id
    ).all()

    # Hardware Info
    hardware = db.query(
        HardwareInfo.cpu_time_used,
        HardwareInfo.duration_ms,
        HardwareInfo.cpu_percent,
        HardwareInfo.memory_used_mb,
        HardwareInfo.created_at,
        HardwareInfo.test_session_id
    ).all()

    return {
        "benchmark_overview": [
            {
                "test_session_id": r.test_session_id,
                "duration_ms": r.duration_ms,
                "success_status": r.success_status,
                "status": r.status,
                "request_id": r.request_id,
                "created_at": r.created_at,
            } for r in benchmark
        ],

        "hardware_info": [
            {
                "test_session_id": r.test_session_id,
                "duration_ms": r.duration_ms,
                "cpu_percent": r.cpu_percent,
                "memory_used_mb": r.memory_used_mb,
                "cpu_time_used": r.cpu_time_used,
                "created_at": r.created_at,
            } for r in hardware
        ]
    }


# -------------------------------
# Aggregierte Statistiken pro TestSession
# -------------------------------
@query_api.get("/stats/by-session")
async def get_stats_by_session(db: Session = Depends(get_db)):
    """
    Aggregierte Statistiken gruppiert nach TestSession
    """
    stats = db.query(
        HardwareInfo.test_session_id,
        func.avg(HardwareInfo.duration_ms).label("avg_duration"),
        func.min(HardwareInfo.duration_ms).label("min_duration"),
        func.max(HardwareInfo.duration_ms).label("max_duration"),
        func.avg(HardwareInfo.cpu_percent).label("avg_cpu"),
        func.avg(HardwareInfo.memory_used_mb).label("avg_memory")
    ).group_by(
        HardwareInfo.test_session_id
    ).all()

    return [
        {
            "test_session_id": s.test_session_id,
            "avg_duration_ms": float(s.avg_duration),
            "min_duration_ms": float(s.min_duration),
            "max_duration_ms": float(s.max_duration),
            "avg_cpu_percent": float(s.avg_cpu),
            "avg_memory_mb": float(s.avg_memory)
        } for s in stats
    ]


# -------------------------------
# Aktuellste Datensätze
# -------------------------------
@query_api.get("/stats/recent")
async def get_recent_results(limit: int = 10, db: Session = Depends(get_db)):
    """
    Holt die neuesten N Ergebnisse
    """
    recent_benchmark = db.query(BenchmarkOverview) \
        .order_by(BenchmarkOverview.created_at.desc()) \
        .limit(limit).all()

    recent_hardware = db.query(HardwareInfo) \
        .order_by(HardwareInfo.created_at.desc()) \
        .limit(limit).all()

    recent_stats = db.query(Statistiken) \
        .order_by(Statistiken.created_at.desc()) \
        .limit(limit).all()

    return {
        "recent_benchmark_overview": recent_benchmark,
        "recent_hardware_info": recent_hardware,
        "recent_statistiken": recent_stats
    }


# -------------------------------
# DELETE Funktionen
# -------------------------------
@query_api.delete("/clear/benchmark")
async def clear_benchmark_overview(db: Session = Depends(get_db)):
    """Löscht alle Benchmark-Übersichtsdaten"""
    count = db.query(BenchmarkOverview).delete()
    db.commit()
    return {"deleted": count}


@query_api.delete("/clear/hardware")
async def clear_hardware_info(db: Session = Depends(get_db)):
    """Löscht alle Hardware-Infos"""
    count = db.query(HardwareInfo).delete()
    db.commit()
    return {"deleted": count}


@query_api.delete("/clear/statistiken")
async def clear_statistiken(db: Session = Depends(get_db)):
    """Löscht alle Statistik-Daten"""
    count = db.query(Statistiken).delete()
    db.commit()
    return {"deleted": count}


@query_api.delete("/clear/all")
async def clear_all_results(db: Session = Depends(get_db)):
    """Löscht alle Testergebnisse"""
    benchmark_count = db.query(BenchmarkOverview).delete()
    hardware_count = db.query(HardwareInfo).delete()
    stats_count = db.query(Statistiken).delete()
    db.commit()

    return {
        "deleted_benchmark_overview": benchmark_count,
        "deleted_hardware_info": hardware_count,
        "deleted_statistiken": stats_count
    }
