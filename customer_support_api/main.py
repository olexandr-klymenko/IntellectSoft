from contextlib import asynccontextmanager

import uvicorn
from core.config import settings
from fastapi import FastAPI

from customer_support_api.db_helper import db_helper
from customer_support_api.models import BaseModel
from customer_support_api.v1.routes.customer_requests import (
    router as requests_router,
)
from customer_support_api.v1.routes.customers import router as customers_router
from customer_support_api.v1.routes.operator import router as operator_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseModel.metadata.create_all(db_helper.engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=customers_router, prefix=settings.api_v1_prefix)
app.include_router(router=requests_router, prefix=settings.api_v1_prefix)
app.include_router(router=operator_router, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


# TODO: Complete API
# TODO: Implement pagination
# TODO: Implement HATEOAS
# TODO: Add docstrings and comments
# TODO: Complete alembic migrations
# TODO: Update README
