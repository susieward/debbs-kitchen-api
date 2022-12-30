from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from app.api.routers import recipes
from app.api.events import create_db, close_db

from app.config import get_settings

def get_app():
    config_settings = get_settings()

    app = FastAPI()
    app.state.config = config_settings

    app.add_middleware(GZipMiddleware, minimum_size=1000)
    #app.mount("/static", StaticFiles(directory = "app/static"), name = "static")

    app.add_event_handler("startup", create_db(app))
    app.add_event_handler("shutdown", close_db(app))

    app.include_router(recipes.router, tags=["recipe"])
    #app.include_router(menus.router, tags=["menu"])
    #app.include_router(drafts.router, tags=["draft"])

    return app

app = get_app()
