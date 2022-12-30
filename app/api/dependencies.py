from databases import Database
from fastapi import Depends, Request

from app.data.recipe import RecipeData
from app.data.menu import MenuData
from app.data.draft import DraftData

from app.logic.recipe import RecipeLogic
from app.logic.menu import MenuLogic
from app.logic.draft import DraftLogic


def get_db(request: Request) -> Database:
    return request.app.state.database

def recipe_data_dep(db: Database = Depends(get_db)) -> RecipeData:
    return RecipeData(db=db)

def menu_data_dep(db: Database = Depends(get_db)) -> RecipeData:
    return MenuData(db=db)

def draft_data_dep(db: Database = Depends(get_db)) -> DraftData:
    return DraftData(db=db)

def recipe_logic_dep(recipe_data: RecipeData = Depends(recipe_data_dep)) -> RecipeLogic:
    return RecipeLogic(recipe_data=recipe_data)

def menu_logic_dep(menu_data: MenuData = Depends(menu_data_dep)) -> MenuLogic:
    return MenuLogic(menu_data=menu_data)

def draft_logic_dep(draft_data: DraftData = Depends(draft_data_dep)) -> DraftLogic:
    return DraftLogic(draft_data=draft_data)
