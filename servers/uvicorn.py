from fastapi import APIRouter
from datetime import datetime
import csv
import os
from pydantic import BaseModel

uvicorn_api = APIRouter()


class RequestModel(BaseModel):
    req_number:int

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


async def async_test():
    print("This is just test.")


@uvicorn_api.post("/get_async_uvicorn_function")
async def get_async_function(req:RequestModel):
    start = datetime.now()
    await async_test()
    end = datetime.now()
    print(req)
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "uvicorn",
               "type": "async",
               "requests":req.req_number,
               "duration_ms": duration_ms}]
    save_result("benchmark_results.csv", result)
    return result


def sync_test():
    print("This is just test.")


@uvicorn_api.post("/get_sync_uvicorn_function")
def get_sync_function (req:RequestModel):
    start = datetime.now()
    sync_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "uvicorn",
               "type": "sync",
               "requests":req.req_number,
               "duration_ms": duration_ms}]
    save_result("benchmark_results.csv", result)
    return result
