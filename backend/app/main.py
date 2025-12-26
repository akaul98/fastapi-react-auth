from fastapi import FastAPI
from app.api.v1.routes import users
from app.api.v1.routes import db



def create_app()->FastAPI:

  app = FastAPI(
    title="First App",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
  )
  

  app.include_router(users.router, prefix="/api/users", tags=["users"])
  app.include_router(db.router)

  return app

app=create_app()  