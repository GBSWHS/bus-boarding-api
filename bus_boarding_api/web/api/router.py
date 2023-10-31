from fastapi.routing import APIRouter

from bus_boarding_api.web.api import docs, echo, monitoring, user, bus, boarding_record, bus_stop

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(boarding_record.router, prefix="/boarding", tags=["boarding"])
api_router.include_router(bus_stop.router, prefix="/stops", tags=["station"]),
api_router.include_router(bus.router, prefix="/bus", tags=["bus"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
