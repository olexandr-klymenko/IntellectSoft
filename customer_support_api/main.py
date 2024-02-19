from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from customer_support_api.config import settings
from customer_support_api.db_helper import db_helper
from customer_support_api.models import BaseModel
from customer_support_api.routes.customers import router as customers_router
from customer_support_api.routes.operator import router as operator_router
from customer_support_api.routes.requests import router as requests_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # As far it is just test task we omit using alembic migrations
    # which is mandatory for real projects
    BaseModel.metadata.create_all(db_helper.engine)
    yield


app = FastAPI(lifespan=lifespan)
add_pagination(app)
app.include_router(router=customers_router, prefix=settings.api_v1_prefix)
app.include_router(router=requests_router, prefix=settings.api_v1_prefix)
app.include_router(router=operator_router, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
