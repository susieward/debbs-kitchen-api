from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import recipes, menus, drafts, instructions, ingredients
from app.api.events import create_db, close_db

from app.config import get_settings

def get_app():
    config_settings = get_settings()

    app = FastAPI()
    app.state.config = config_settings

    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config_settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    #app.mount("/static", StaticFiles(directory = "app/static"), name = "static")

    app.add_event_handler("startup", create_db(app))
    app.add_event_handler("shutdown", close_db(app))

    app.include_router(recipes.router, tags=["recipe"])
    app.include_router(menus.router, tags=["menu"])
    app.include_router(drafts.router, tags=["draft"])
    app.include_router(instructions.router, tags=["instruction"])
    app.include_router(ingredients.router, tags=["ingredients"])

    return app

app = get_app()
