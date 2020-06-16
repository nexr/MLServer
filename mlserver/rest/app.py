from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.responses import ORJSONResponse

from .endpoints import Endpoints

from ..settings import Settings
from ..handlers import DataPlane


def create_app(settings: Settings, data_plane: DataPlane) -> FastAPI:
    endpoints = Endpoints(data_plane)
    routes = [
        APIRoute("/v2/health/live", endpoints.live),
        APIRoute("/v2/health/ready", endpoints.ready),
        APIRoute(
            "/v2/models/{model_name}/versions/{model_version}/ready",
            endpoints.model_ready,
        ),
        APIRoute(
            "/v2/models/{model_name}/versions/{model_version}/infer",
            endpoints.infer,
            methods=["POST"],
        ),
    ]

    app = FastAPI(
        debug=settings.debug, routes=routes, default_response_class=ORJSONResponse
    )

    return app