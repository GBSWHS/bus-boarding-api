from fastapi.routing import APIRouter

from bus_boarding_api.web.api import docs, echo, monitoring, redis, user, bus

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(bus.router, prefix="/bus", tags=["bus"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
