from databases import Database
from fastapi import Depends, Request

from app.data.recipe import RecipeData
from app.data.menu import MenuData
from app.data.draft import DraftData
from app.data.instruction import InstructionData
from app.data.ingredient import IngredientData

from app.logic.recipe import RecipeLogic
from app.logic.menu import MenuLogic
from app.logic.draft import DraftLogic
from app.logic.instruction import InstructionLogic
from app.logic.ingredient import IngredientLogic


def get_db(request: Request) -> Database:
    return request.app.state.database

def instruction_data_dep(db: Database = Depends(get_db)) -> InstructionData:
    return InstructionData(db=db)

def ingredient_data_dep(db: Database = Depends(get_db)) -> IngredientData:
    return IngredientData(db=db)

def recipe_data_dep(db: Database = Depends(get_db),
    instruction_data = Depends(instruction_data_dep),
    ingredient_data = Depends(ingredient_data_dep)
) -> RecipeData:
    return RecipeData(db=db, instruction_data=instruction_data, ingredient_data=ingredient_data)

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

def instruction_logic_dep(instruction_data: InstructionData = Depends(instruction_data_dep)) -> InstructionLogic:
    return InstructionLogic(instruction_data=instruction_data)

def ingredient_logic_dep(ingredient_data: IngredientData = Depends(ingredient_data_dep)) -> IngredientLogic:
    return IngredientLogic(ingredient_data=ingredient_data)
