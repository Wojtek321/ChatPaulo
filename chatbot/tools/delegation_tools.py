from pydantic import BaseModel


class MenuInfoTool(BaseModel):
    """Use this tool when the customer inquires about the menu, ingredients, or any other food-related information at the pizzeria."""


class OrderManagementTool(BaseModel):
    """Use this tool when a customer wants to place an order, modify an existing one, cancel an order, or needs assistance with the ordering process."""


class CompleteOrEscalate(BaseModel):
    """
    A tool to mark the current task as resolved or to escalate it for further handling when additional input or action is required.
    Use this when the task is completed successfully or cannot proceed due to specific reason.
    """
