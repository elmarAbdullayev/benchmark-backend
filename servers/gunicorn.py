import asyncio

from fastapi import APIRouter
from datetime import datetime
import psutil
from servers.uvicorn import save_hardware_result

gunicorn_api = APIRouter()

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

@gunicorn_api.get("/get_async_gunicorn_function")
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

    # CPU-Zeit berechnen
    cpu_time_used = (cpu_times_end.user - cpu_times_start.user) + \
                    (cpu_times_end.system - cpu_times_start.system)

    duration_ms = (end - start).total_seconds() * 1000

    # CPU-Prozentsatz
    cpu_percent = (cpu_time_used / (duration_ms / 1000) * 100) if duration_ms > 0 else 0

    # Speicherwerte
    memory_used_mb = memory_info_end.rss / 1024 / 1024
    memory_diff_mb = (memory_info_end.rss - memory_info_start.rss) / 1024 / 1024
    memory_vms_mb = memory_info_end.vms / 1024 / 1024

    hardware_result = [{
        "server": "gunicorn",
        "type": "async",
        "cpu_time_used": cpu_time_used,
        "duration_ms": duration_ms,
        "cpu_percent": cpu_percent,
        "memory_used_mb": memory_used_mb,
        "memory_diff_mb": memory_diff_mb,
        "memory_vms_mb": memory_vms_mb
    }]
    save_hardware_result("hardware_result.csv", hardware_result)

    result = [{
        "server": "gunicorn",
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


@gunicorn_api.get("/get_sync_gunicorn_function")
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

    # CPU-Zeit berechnen
    cpu_time_used = (cpu_times_end.user - cpu_times_start.user) + \
                    (cpu_times_end.system - cpu_times_start.system)

    duration_ms = (end - start).total_seconds() * 1000

    # CPU-Prozentsatz
    cpu_percent = (cpu_time_used / (duration_ms / 1000) * 100) if duration_ms > 0 else 0

    # Speicherwerte
    memory_used_mb = memory_info_end.rss / 1024 / 1024
    memory_diff_mb = (memory_info_end.rss - memory_info_start.rss) / 1024 / 1024
    memory_vms_mb = memory_info_end.vms / 1024 / 1024

    hardware_result = [{
        "server": "gunicorn",
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
        "server": "gunicorn",
        "type": "sync",
        "duration_ms": duration_ms
    }]
    return result
