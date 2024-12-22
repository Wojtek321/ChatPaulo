from langchain_core.tools import tool
import requests
from typing import List, Dict, Any, Annotated
from pydantic import BaseModel, Field


API_ENDPOINT = 'http://django:8000/api/'

CHATBOT_BEARER_TOKEN = "SUPER_SECRET_TOKEN"


@tool
def fetch_order(
    order_id: Annotated[int, 'The unique identifier (ID) of the order']
) -> Dict[str, Any]:
    """
    Retrieves information about a specific order placed, based on the unique ID provided.
    Useful when information on a specific order are needed.
    This function is not intended for creating or updating orders.
    Returns a dictionary containing order data such as ID, order type, items ordered, total price.
    """
    response = requests.get(API_ENDPOINT + f'orders/{order_id}/')
    return response.json()


class Item(BaseModel):
    item: str = Field(description='A unique identifier ID for the menu item.')
    quantity: int = Field(1, description='The number of units for item.')
    detail_note: str = Field(None, description='An optional note providing additional details.')


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

    response = requests.post(API_ENDPOINT + 'orders/', json=data, headers={'Authorization': f'Bearer {CHATBOT_BEARER_TOKEN}'})
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

    response = requests.post(API_ENDPOINT + 'orders/', json=data, headers={'Authorization': f'Bearer {CHATBOT_BEARER_TOKEN}'})
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

    response = requests.post(API_ENDPOINT + 'orders/', json=data, headers={'Authorization': f'Bearer {CHATBOT_BEARER_TOKEN}'})
    return response.json()


@tool
def update_order(
    order_id: Annotated[int, 'The unique identifier (ID) of the order'],
    customer_name: Annotated[str, 'The name of customer placing an order.'] = None,
    customer_phone: Annotated[str, 'Customer contact phone number.'] = None,
    address: Annotated[str, 'The full delivery address where the order should be sent.'] = None,
    order_note: Annotated[str, 'Note for the entire order, which can include additional instructions or requests.'] = None,
    items: Annotated[List[Item], 'A list of menu items being ordered. This should be the complete list of items for the order.'] = None,
) -> Dict[str, Any]:
    """
    Updates an exising order.
    Useful when a customer changes their mind about a placed order, such as modifying the items, adding a note, or updating customer information.
    This function is intended for updating orders already placed and should not be used for creating new orders.
    Returns a dictionary containing details of the updated order.
    """
    data = {}

    if customer_name is not None:
        data['customer_name'] = customer_name
    if customer_phone is not None:
        data['customer_phone'] = customer_phone
    if address is not None:
        data['address'] = address
    if order_note is not None:
        data['order_note'] = order_note
    if items is not None:
        data['items'] = [item.model_dump(mode='json') for item in items]

    if not data:
        raise ValueError('At least one filed must be provided for update.')

    response = requests.patch(API_ENDPOINT + f'orders/{order_id}/', json=data, headers={'Authorization': f'Bearer {CHATBOT_BEARER_TOKEN}'})
    return response.json()


@tool
def cancel_order(
    order_id: Annotated[int, 'The unique identifier (ID) of the order']
) -> Dict[str, Any]:
    """
    Deletes a specific order, based on the unique ID provided.
    Useful when a customer wants to cancel or remove an order.
    This function is not intended for creating or updating orders.
    Returns a dictionary with a success message or error details.
    """
    response = requests.delete(API_ENDPOINT + f'orders/{order_id}/', headers={'Authorization': f'Bearer {CHATBOT_BEARER_TOKEN}'})

    if response.status_code == 204:
        return {'message': 'Order successfully deleted.'}
    else:
        return response.json()
