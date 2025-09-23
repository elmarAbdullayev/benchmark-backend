from fastapi import APIRouter
from datetime import datetime
from servers.uvicorn import save_result
from servers.uvicorn import RequestModel


gunicorn_api = APIRouter()

async def async_test():
    print("This is async test.")


@gunicorn_api.post("/get_async_gunicorn_function")
async def get_async_function (req:RequestModel):
    start = datetime.now()
    await async_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "gunicorn",
               "type": "async",
               "requests":req.req_number,
               "duration_ms": duration_ms}]
    save_result("benchmark_results.csv", result)
    return result



def sync_test():
    print("This is sync test.")


@gunicorn_api.post("/get_sync_gunicorn_function")
def get_sync_function (req:RequestModel):
    start = datetime.now()
    sync_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "gunicorn",
               "type": "async",
               "requests":req.req_number,
               "duration_ms": duration_ms}]
    save_result("benchmark_results.csv", result)
    return result


@gunicorn_api.get("/get_sync_gunicorn_function")
async def get_async_function ():
    start = datetime.now()
    await async_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "gunicorn",
               "type": "async",

               "duration_ms": duration_ms}]
    save_result("benchmark_results.csv", result)
    return result