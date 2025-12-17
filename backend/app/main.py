from fastapi import FastAPI
from .routes import users



def create_app()->FastAPI:

  app = FastAPI(
    title="First App",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
  )
  

  app.include_router(users.router)
#  app.include_router(auth.router)

  return app

app=create_app()  