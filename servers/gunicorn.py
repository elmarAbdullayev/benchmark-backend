from fastapi import APIRouter
from datetime import datetime

gunicorn_api = APIRouter()

async def async_test():
    print("This is async test.")
x=0

@gunicorn_api.get("/get_async_gunicorn_function")
async def get_async_function ():
    global x
    x += 1
    print(x)
    start = datetime.now()
    await async_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "gunicorn",
               "type": "async",
               "duration_ms": duration_ms}]
    return result

def sync_test():
    print("This is sync testttttt.")


@gunicorn_api.get("/get_sync_gunicorn_function")
def get_sync_function ():
    global x
    x += 1
    print("aaaaaaaa",x)
    start = datetime.now()
    sync_test()
    end = datetime.now()
    duration_ms = (end - start).total_seconds() * 1000
    result = [{"server": "gunicorn",
               "type": "sync",
               "duration_ms": duration_ms}]
    return result


