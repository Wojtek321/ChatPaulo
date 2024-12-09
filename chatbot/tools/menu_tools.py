from langchain_core.tools import tool
import requests
from typing import List, Dict, Any, Annotated


API_ENDPOINT = 'http://localhost:8000/api/'


@tool
def fetch_full_menu() -> List[Dict[str, Any]]:
    """
    Retrieves a complete list of items available on the pizzeria's menu.
    It is useful when there is a need to retrieve a comprehensive overview of all offerings,
    such as presenting the entire menu.
    It should not be used for retrieving information about ingredient or orders.
    Returns list of items, each item contains: ID, name, type, price, and description.
    """
    response = requests.get(API_ENDPOINT + 'items/')
    return response.json()


@tool
def fetch_item_ingredients(
    i: Annotated[int, 'The unique identifier (ID) of the menu item']
) -> Dict[str, Any]:
    """
    Provides information about a specific menu item based on its unique identifier.
    It is suitable for retrieving a list of ingredients, along with other details such as name, price, and description.
    It is not intended for general contextual information about pizza or for querying the entire menu.
    This function returns dictionary containing item ID, name, type, price, description, and list of ingredients.
    """
    response = requests.get(API_ENDPOINT + f'items/{i}/')
    return response.json()


@tool
def fetch_ingredient_list() -> List[Dict[str, Any]]:
    """
    Provides a complete list of ingredients used in the pizzeria menu items.
    Useful for answering general questions about the ingredients available at the pizzeria.
    It is not suitable for retrieving information about list of ingredients in a particular product.
    Returns list od dictionaries, where each dictionary contains the ingredient ID, name, and descriptions.
    """
    response = requests.get(API_ENDPOINT + 'ingredients/')
    return response.json()


@tool
def fetch_ingredient(
    i: Annotated[int, 'The unique identifier (ID) of the ingredient']
) -> Dict[str, Any]:
    """
    Retrieves information about a specific ingredients based on the unique ID provided.
    It is helpful when data about particular ingredient is needed.
    This function should not be used for listing all ingredients.
    Returns a dictionary containing ingredient data: ID, name, and description.
    """
    response = requests.get(API_ENDPOINT + f'ingredients/{i}/')
    return response.json()
