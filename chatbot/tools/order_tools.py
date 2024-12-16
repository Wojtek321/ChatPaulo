from langchain_core.tools import tool
import requests
from typing import List, Dict, Any, Annotated
from pydantic import BaseModel, Field


API_ENDPOINT = 'http://django:8000/api/'


@tool
def fetch_order(
    i: Annotated[int, 'The unique identifier (ID) of the order']
) -> Dict[str, Any]:
    """
    Retrieves information about a specific order placed, based on the unique ID provided.
    Useful when information on a specific order are needed.
    This function is not intended for creating or updating orders.
    Returns a dictionary containing order data such as ID, order type, items ordered, total price.
    """
    response = requests.get(API_ENDPOINT + f'orders/{i}/')
    return response.json()


class Item(BaseModel):
    item: str = Field(description='A unique identifier ID for the menu item.')
    quantity: int = Field(1, description='The number of units for item.')
    detailed_note: str = Field(None, description='An optional note providing additional details.')


@tool
def place_on_site_order(
    items: Annotated[List[Item], 'A list of menu items being ordered.'],
    order_note: Annotated[str, 'Note for the entire order, which can include additional instructions or requests.'] = None,
) -> Dict[str, Any]:
    """
    Places an on-site order for the pizzeria, intended for customer dining at the location.
    Use this function fot placing orders that will be served at the restaurant table.
    It should not be used for creating pick-up or delivery orders.
    Returns a dictionary containing details of the created order, including order ID, items ordered, total price.
    """
    items = [item.model_dump(mode='json') for item in items]
    data = {
        'order_type': 'on-site',
        'items': items,
        'order_note': order_note,
    }

    response = requests.post(API_ENDPOINT + 'orders/', json=data)
    return response.json()


@tool
def place_pickup_order(
    items: Annotated[List[Item], 'A list of menu items being ordered.'],
    customer_name: Annotated[str, 'The name of customer placing an order.'],
    customer_phone: Annotated[str, 'Customer contact phone number.'],
    order_note: Annotated[str, 'Note for the entire order, which can include additional instructions or requests.'] = None,
) -> Dict[str, Any]:
    """
    Places a pick-up order at the pizzeria for customer collecting their meals in person.
    Useful when customer wants to place an order and pick it up from the pizzeria themselves.
    Not intended when customer will be dining at the pizzeria or order delivered to and address is needed.
    Returns a dictionary containing details of the created order, including order ID, items ordered, total price, pick-up time.
    """
    items = [item.model_dump(mode='json') for item in items]
    data = {
        'order_type': 'pick-up',
        'items': items,
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'order_note': order_note,
    }

    response = requests.post(API_ENDPOINT + 'orders/', json=data)
    return response.json()


@tool
def place_delivery_order(
    items: Annotated[List[Item], 'A list of menu items being ordered.'],
    customer_name: Annotated[str, 'The name of customer placing an order.'],
    customer_phone: Annotated[str, 'Customer contact phone number.'],
    address: Annotated[str, 'The full delivery address where the order should be sent.'],
    order_note: Annotated[str, 'Note for the entire order, which can include additional instructions or requests.'] = None,
) -> Dict[str, Any]:
    """
    Places a delivery order for customers who require their meals to be delivered to a specified address.
    Useful when customer wants their order delivered to a specific address.
    Do not use this function when customer wants to pick up the order themselves or dine at the pizzeria.
    Returns a dictionary containing details of the created order, including order ID, items ordered, total price, delivery time.
    """
    items = [item.model_dump(mode='json') for item in items]
    data = {
        'order_type': 'delivery',
        'items': items,
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'address': address,
        'order_note': order_note,
    }

    response = requests.post(API_ENDPOINT + 'orders/', json=data)
    return response.json()
