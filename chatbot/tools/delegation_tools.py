from pydantic import BaseModel


class MenuInfoTool(BaseModel):
    """Use this tool when the customer inquires about the menu, ingredients, or any other food-related information at the pizzeria."""


class OrderManagementTool(BaseModel):
    """
    Use this tool when a customer wants to place an order, modify an existing one, or needs assistance with the ordering process.
    It can also be used to provide support for order-related issues, such as modifications or cancellations.
    """


class CompleteOrEscalate(BaseModel):
    """
    A tool to mark the current task as resolved or to escalate it for further handling when additional input or action is required.
    Use this when the task is completed successfully or cannot proceed due to specific reason.
    """
    completed: bool = True
    reason: str

    class Config:
        json_schema_extra = {
            'example': {
                'cancel': True,
                'reason': 'User changed their mind about the current task.'
            },
            'example 2': {
                'cancel': True,
                'reason': 'I have fully completed the task.'
            },
            'example 3': {
                'cancel': False,
                'reason': 'An error occurred when calling the function.'
            }
        }