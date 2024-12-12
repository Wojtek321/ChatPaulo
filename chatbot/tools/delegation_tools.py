from pydantic import BaseModel



class ToMenuAssistant(BaseModel):
    """Use this tool when the customer inquires about the menu, ingredients, or any other food-related information at the pizzeria."""


class ToOrderAssistant(BaseModel):
    """
    Use this tool when a customer wants to place an order, modify an existing one, or needs assistance with the ordering process.
    It can also be used to provide support for order-related issues, such as modifications or cancellations.
    """
