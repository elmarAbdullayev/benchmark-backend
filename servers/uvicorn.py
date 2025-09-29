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


async def async_test():
    print("This is just testttttt.")

x=0

@uvicorn_api.get("/get_async_uvicorn_function")
async def get_async_function():
    global x
    x += 1
    print(x)
    start = datetime.now()
    await async_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "uvicorn",
               "type": "async",
               "duration_ms": duration_ms}]
    return result


def sync_test():
    print("This is just test.")


@uvicorn_api.get("/get_sync_uvicorn_function")
def get_sync_function ():
    global x
    x += 1
    print(x)
    start = datetime.now()
    sync_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "uvicorn",
               "type": "sync",
               "duration_ms": duration_ms,
               }]
    return result
