import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.routes import auth, otp, organization, users
from app.config import settings
from app.limiter import limiter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

_SENSITIVE_HEADERS = {"authorization", "cookie"}


def create_app() -> FastAPI:
    logger.info("Creating FastAPI application...")

    app = FastAPI(
        title="First App",
        version="1.0.0",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        debug=settings.DEBUG,
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.debug(f"Request: {request.method} {request.url}")
        safe_headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in _SENSITIVE_HEADERS
        }
        logger.debug(f"Headers: {safe_headers}")
        response = await call_next(request)
        logger.debug(f"Response status: {response.status_code}")
        return response

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    app.include_router(users.router, prefix="/api/users", tags=["users"])
    app.include_router(organization.router, prefix="/api/organizations", tags=["organizations"])
    app.include_router(otp.router, prefix="/api/otp", tags=["otp"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

    logger.info("FastAPI application created successfully")
    return app


app = create_app()
