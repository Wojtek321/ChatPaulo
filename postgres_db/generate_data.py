from typing import Optional, List
from pydantic import BaseModel
from openai import OpenAI
from pprint import pprint
import json


client = OpenAI()

pizza_names = [
    'Margherita',
    'Pepperoni',
    'Hawaiian',
    'Neapoletana',
    'Capricciosa',
    'Romana',
    'Carbonara',
    'Vegetariana',
    'Four Cheese',
    'Caprese',
]

system_prompt = "You are highly knowledgeable culinary assistant with deep expertise in pizzas nad beverages. " \
                "Your task is to provide comprehensive and accurate responses to user queries. " \
                "Focus on delivering natural and informative content that is enjoyable to read."


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    type: str

class ItemList(BaseModel):
    items: List[Item]


completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a list of 10 pizzas and 5 beverages, including their names, brief descriptions, and prices in dollars. Use the following pizza names: {pizza_names}."}
    ],
    response_format=ItemList,
)

items = completion.choices[0].message.parsed
pprint(items.items)

with open('data/items.json', 'w') as f:
    json.dump(items.model_dump(mode='json'), f, indent=4)



class Ingredient(BaseModel):
    id: int
    name: str
    description: Optional[str]

class IngredientList(BaseModel):
    ingredients: List[Ingredient]


completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Provide a list of ingredients used to prepare the following pizzas: {pizza_names}. For each ingredient provide its name and brief description."}
    ],
    response_format=IngredientList,
)

ingredients = completion.choices[0].message.parsed
pprint(ingredients.ingredients)

with open('data/ingredients.json', 'w') as f:
    json.dump(ingredients.model_dump(mode='json'), f, indent=4)



class Recipe(BaseModel):
    item_id: int
    ingredient_id: int
    quantity: int
    unit: str

class RecipeList(BaseModel):
    recipes: List[Recipe]


completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Create recipes by assigning ingredients to each pizza. Specify the ingredient quantity.\n"
                                    f"Items: {items}\n"
                                    f"Ingredients: {ingredients}."}
    ],
    response_format=RecipeList,
)

recipes = completion.choices[0].message.parsed
pprint(recipes.recipes)

with open('data/recipes.json', 'w') as f:
    json.dump(recipes.model_dump(mode='json'), f, indent=4)