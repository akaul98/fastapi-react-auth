import logging
from fastapi import FastAPI
from app.api.v1.routes import users
from app.api.v1.routes import organization
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

orgins=["*"]




def create_app()->FastAPI:
  logger.info("Creating FastAPI application...")

  app = FastAPI(
    title="First App",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    debug=True,
  )

  app.add_middleware(
      CORSMiddleware,
      allow_origins=orgins,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )


  # Middleware for logging requests (useful for debugging)
  @app.middleware("http")
  async def log_requests(request, call_next):
      logger.debug(f"Request: {request.method} {request.url}")
      logger.debug(f"Headers: {request.headers}")
      response = await call_next(request)
      logger.debug(f"Response status: {response.status_code}")
      return response

  app.include_router(users.router, prefix="/api/users", tags=["users"])
  app.include_router(organization.router, prefix="/api/organizations", tags=["organizations"])

  logger.info("FastAPI application created successfully")
  return app

app=create_app()  