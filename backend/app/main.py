from fastapi import FastAPI
from .routes import users
from .routes import db
from .schema import user



def create_app()->FastAPI:

  app = FastAPI(
    title="First App",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
  )
  

  app.include_router(users.router)
  app.include_router(db.router)

  return app

app=create_app()  