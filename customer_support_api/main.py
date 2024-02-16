from contextlib import asynccontextmanager

import uvicorn
from core.config import settings
from fastapi import FastAPI
from v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


@app.get("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


# TODO: Finish crud function
# TODO: Complete API
# TODO: Implement pagination
# TODO: Implement HATEOAS
# TODO: Add docstrings and comments
# TODO: Complete alembic migrations
# TODO: Update README
