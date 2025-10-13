import asyncio

from fastapi import APIRouter
from datetime import datetime
import csv
import os
from pydantic import BaseModel

uvicorn_api = APIRouter()


class RequestModel(BaseModel):
    success_status:bool
    status:int
    id:int
    type:str
    server:str

def save_hardware_result(filename, data):
    base_dir = os.getcwd()
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        open(filepath, "w").close()

    keys = data[0].keys()
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(data)

def save_result(filename, data):
    base_dir = os.getcwd()
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        open(filepath, "w").close()

    keys = data[0].keys()
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(data)

@uvicorn_api.post("/save_result")
async def data_saving(dat:RequestModel):
    start = datetime.now()
    await async_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": dat.server,
                "type": dat.type,
                "duration_ms": duration_ms,
                "success_status": dat.success_status,
                "status": dat.status,
                "id": dat.id}]
    save_result("benchmark_results.csv", result)
    return result

import psutil


def cpu_heavy_task():
    data = []
    for i in range(10_000_000):
        _ = i * i
        if i % 1000 == 0:
            data.append([i] * 100)
    return data  # Wichtig: nicht sofort freigeben

async def async_test():
    result = await asyncio.to_thread(cpu_heavy_task)
    await asyncio.sleep(0.1)
    return result


@uvicorn_api.get("/get_async_uvicorn_function")
async def get_async_function():
    process = psutil.Process()

    # CPU-Zeiten und Speicher VOR der Operation
    cpu_times_start = process.cpu_times()
    memory_info_start = process.memory_info()
    start = datetime.now()

    # Die eigentliche Operation
    await async_test()

    # CPU-Zeiten und Speicher NACH der Operation
    end = datetime.now()
    cpu_times_end = process.cpu_times()
    memory_info_end = process.memory_info()

    # CPU-Zeit berechnen (user + system time in Sekunden)
    cpu_time_used = (cpu_times_end.user - cpu_times_start.user) + \
                    (cpu_times_end.system - cpu_times_start.system)

    duration_ms = (end - start).total_seconds() * 1000

    # CPU-Prozentsatz für diesen spezifischen Request
    cpu_percent = (cpu_time_used / (duration_ms / 1000) * 100) if duration_ms > 0 else 0

    # Speicher-Metriken berechnen
    memory_used_mb = memory_info_end.rss / 1024 / 1024  # RSS in MB
    memory_diff_mb = (memory_info_end.rss - memory_info_start.rss) / 1024 / 1024  # Differenz in MB
    memory_vms_mb = memory_info_end.vms / 1024 / 1024  # Virtual Memory Size in MB

    hardware_result = [{
    "server": "uvicorn",
    "type": "async",
    "cpu_time_used": cpu_time_used,
    "duration_ms": duration_ms,
    "cpu_percent": cpu_percent,
    "memory_used_mb": memory_used_mb,
    "memory_diff_mb": memory_diff_mb,
    "memory_vms_mb": memory_vms_mb
}]
    save_hardware_result("hardware_result.csv",hardware_result)

    result = [{
        "server": "uvicorn",
        "type": "async",
        "duration_ms": duration_ms
    }]
    return result



def sync_test():
    data = []
    for i in range(10_000_000):
        _ = i * i
        if i % 1000 == 0:
            data.append([i] * 100)
    return data


@uvicorn_api.get("/get_sync_uvicorn_function")
def get_sync_function():
    process = psutil.Process()

    # CPU-Zeiten und Speicher VOR der Operation
    cpu_times_start = process.cpu_times()
    memory_info_start = process.memory_info()
    start = datetime.now()

    # Die eigentliche Operation
    sync_test()

    # CPU-Zeiten und Speicher NACH der Operation
    end = datetime.now()
    cpu_times_end = process.cpu_times()
    memory_info_end = process.memory_info()

    # CPU-Zeit berechnen (user + system time in Sekunden)
    cpu_time_used = (cpu_times_end.user - cpu_times_start.user) + \
                    (cpu_times_end.system - cpu_times_start.system)

    duration_ms = (end - start).total_seconds() * 1000

    # CPU-Prozentsatz für diesen spezifischen Request
    cpu_percent = (cpu_time_used / (duration_ms / 1000) * 100) if duration_ms > 0 else 0

    # Speicher-Metriken berechnen
    memory_used_mb = memory_info_end.rss / 1024 / 1024  # RSS in MB
    memory_diff_mb = (memory_info_end.rss - memory_info_start.rss) / 1024 / 1024  # Differenz in MB
    memory_vms_mb = memory_info_end.vms / 1024 / 1024  # Virtual Memory Size in MB

    hardware_result = [{
        "server": "uvicorn",
        "type": "sync",
        "cpu_time_used": cpu_time_used,
        "duration_ms": duration_ms,
        "cpu_percent": cpu_percent,
        "memory_used_mb": memory_used_mb,
        "memory_diff_mb": memory_diff_mb,
        "memory_vms_mb": memory_vms_mb
    }]
    save_hardware_result("hardware_result.csv", hardware_result)

    result = [{
        "server": "uvicorn",
        "type": "sync",
        "duration_ms": duration_ms
    }]
    return result

