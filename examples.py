from enum import Enum
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel


class ModelName(str, Enum):
    modelA = "A"
    modelB = "B"
    modelC = "C"


class Item(BaseModel):
    name: str
    description: Optional[str] = None


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.modelA:
        return {"model_name": model_name, "message": "Ayyy"}

    return {"model_name": model_name, "message": "B or C!"}


@app.get("/items/")
async def read_item(
        skip: int = 0,
        limit: int = 10,
        nope: bool = False,
        extra: Optional[str] = Query(
            None,
            min_length=2,
            max_length=3,
            regex="^1\\d\\d$",
            title="Parameter title",
            description="Some description of use",
            alias="extra-with-dash"
        ),
):
    if nope:
        return "It's true!"

    if extra:
        return extra

    return fake_items_db[skip: skip + limit]


@app.post("/items/")
async def create_item(item: Item):
    return f'{item.name} was created'
