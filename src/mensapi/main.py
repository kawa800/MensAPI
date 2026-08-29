from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Meal(BaseModel):
    name: str
    date: str
    price: list[int]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/meals")
async def get_meals():
    return {"meal": "curry"}
