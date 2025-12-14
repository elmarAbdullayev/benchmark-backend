# uvicorn_api.py
import asyncio
import psutil
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import os, csv
import pandas as pd
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, TestSession, BenchmarkOverview, HardwareInfo, Statistiken

uvicorn_api = APIRouter()

# 🔹 Request-Datenmodell
class RequestModel(BaseModel):
    test_session_id: int
    success_status: bool
    status: int
    request_id: int
    duration_ms: float

# 🔹 CSV speichern (append falls existiert)
def save_to_csv(filename, data):
    filepath = os.path.join(os.getcwd(), filename)
    file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

# 🔹 Benchmark-Ergebnisse speichern
@uvicorn_api.post("/save_result")
async def save_result(dat: RequestModel, db: Session = Depends(get_db)):
    session = db.query(TestSession).filter(TestSession.id == dat.test_session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session nicht gefunden")

    csv_data = {
        "test_session_id": dat.test_session_id,
        "server": session.server,
        "type": session.type,
        "duration_ms": dat.duration_ms,
        "success_status": dat.success_status,
        "status": dat.status,
        "request_id": dat.request_id
    }
    save_to_csv("benchmark_overview.csv", [csv_data])

    benchmark = BenchmarkOverview(
        test_session_id=dat.test_session_id,
        duration_ms=dat.duration_ms,
        success_status=dat.success_status,
        status=dat.status,
        request_id=dat.request_id
    )
    db.add(benchmark)
    db.commit()
    return {"status": "ok"}

# 🔹 CSV auswerten und Statistik berechnen
@uvicorn_api.get("/show_avg")
async def show_avg(db: Session = Depends(get_db)):
    file = "benchmark_overview.csv"
    if not os.path.exists(file):
        return {"error": "Keine Daten"}

    df = pd.read_csv(file)
    if df.empty:
        return {"error": "CSV leer"}

    df["error_rate"] = (df["status"] != 200).astype(int)
    summary = df.groupby(["test_session_id"]).agg(
        avg_response_time=("duration_ms", "mean"),
        min_response_time=("duration_ms", "min"),
        max_response_time=("duration_ms", "max"),
        avg_error_rate=("error_rate", "mean"),
    ).reset_index()
    summary.to_csv("statistiken_results.csv", index=False)

    # 🔹 Datenbank aktualisieren
    for _, row in summary.iterrows():
        test_session_id = int(row["test_session_id"])
        db.query(Statistiken).filter(Statistiken.test_session_id == test_session_id).delete()
        stat = Statistiken(
            test_session_id=test_session_id,
            avg_response_time=float(row["avg_response_time"]),
            min_response_time=float(row["min_response_time"]),
            max_response_time=float(row["max_response_time"]),
            avg_error_rate=float(row["avg_error_rate"])
        )
        db.add(stat)
    db.commit()
    return summary.to_dict(orient="records")

# 🔹 CPU-intensive Aufgabe (Sync)
def cpu_heavy_task():
    data = []
    for i in range(10_000_000):
        _ = i * i
        if i % 1000 == 0:
            data.append([i] * 100)
    return data

async def async_test():
    result = await asyncio.to_thread(cpu_heavy_task)
    await asyncio.sleep(0.1)
    return result

def sync_test():
    return cpu_heavy_task()

# 🔹 Async Funktion
@uvicorn_api.get("/get_async_uvicorn_function")
async def get_async_function(test_session_id: int = None, db: Session = Depends(get_db)):
    # Session erstellen oder existierende nutzen
    if test_session_id:
        new_session = db.query(TestSession).filter(TestSession.id == test_session_id).first()
        if not new_session:
            raise HTTPException(status_code=404, detail="Session nicht gefunden")
    else:
        new_session = TestSession(server="uvicorn", type="async", num_requests=1)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    session_id = new_session.id

    # 🔹 Ressourcen messen
    process = psutil.Process()
    cpu_start = process.cpu_times()
    mem_start = process.memory_info()
    time_start = datetime.now()

    await async_test()

    time_end = datetime.now()
    new_session.finished_at = time_end
    db.commit()

    cpu_end = process.cpu_times()
    mem_end = process.memory_info()
    cpu_time_used = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
    duration_ms = (time_end - time_start).total_seconds() * 1000
    cpu_percent = (cpu_time_used / (duration_ms / 1000) * 100) if duration_ms > 0 else 0
    memory_used_mb = mem_end.rss / 1024 / 1024
    memory_diff_mb = (mem_end.rss - mem_start.rss) / 1024 / 1024
    memory_vms_mb = mem_end.vms / 1024 / 1024

    # 🔹 Hardware-Daten speichern
    hardware_data = {
        "test_session_id": session_id,
        "server": "uvicorn",
        "type": "async",
        "cpu_time_used": cpu_time_used,
        "duration_ms": duration_ms,
        "cpu_percent": cpu_percent,
        "memory_used_mb": memory_used_mb,
        "memory_diff_mb": memory_diff_mb,
        "memory_vms_mb": memory_vms_mb
    }
    save_to_csv("hardware_info.csv", [hardware_data])

    hardware = HardwareInfo(
        test_session_id=session_id,
        cpu_time_used=cpu_time_used,
        duration_ms=duration_ms,
        cpu_percent=cpu_percent,
        memory_used_mb=memory_used_mb,
        memory_diff_mb=memory_diff_mb,
        memory_vms_mb=memory_vms_mb
    )
    db.add(hardware)
    db.commit()

    return {
        "session_id": session_id,
        "server": "uvicorn",
        "type": "async",
        "duration_ms": duration_ms
    }

# 🔹 Sync Funktion
@uvicorn_api.get("/get_sync_uvicorn_function")
def get_sync_function(test_session_id: int = None, db: Session = Depends(get_db)):
    if test_session_id:
        new_session = db.query(TestSession).filter(TestSession.id == test_session_id).first()
        if not new_session:
            raise HTTPException(status_code=404, detail="Session nicht gefunden")
    else:
        new_session = TestSession(server="uvicorn", type="sync", num_requests=1)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    session_id = new_session.id
    process = psutil.Process()
    cpu_start = process.cpu_times()
    mem_start = process.memory_info()
    time_start = datetime.now()

    sync_test()

    time_end = datetime.now()
    new_session.finished_at = time_end
    db.commit()

    cpu_end = process.cpu_times()
    mem_end = process.memory_info()
    cpu_time_used = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
    duration_ms = (time_end - time_start).total_seconds() * 1000
    cpu_percent = (cpu_time_used / (duration_ms / 1000) * 100) if duration_ms > 0 else 0
    memory_used_mb = mem_end.rss / 1024 / 1024
    memory_diff_mb = (mem_end.rss - mem_start.rss) / 1024 / 1024
    memory_vms_mb = mem_end.vms / 1024 / 1024

    hardware_data = {
        "test_session_id": session_id,
        "server": "uvicorn",
        "type": "sync",
        "cpu_time_used": cpu_time_used,
        "duration_ms": duration_ms,
        "cpu_percent": cpu_percent,
        "memory_used_mb": memory_used_mb,
        "memory_diff_mb": memory_diff_mb,
        "memory_vms_mb": memory_vms_mb
    }
    save_to_csv("hardware_info.csv", [hardware_data])

    hardware = HardwareInfo(
        test_session_id=session_id,
        cpu_time_used=cpu_time_used,
        duration_ms=duration_ms,
        cpu_percent=cpu_percent,
        memory_used_mb=memory_used_mb,
        memory_diff_mb=memory_diff_mb,
        memory_vms_mb=memory_vms_mb
    )
    db.add(hardware)
    db.commit()

    return {
        "session_id": session_id,
        "server": "uvicorn",
        "type": "sync",
        "duration_ms": duration_ms
    }
