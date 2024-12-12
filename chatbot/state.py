from typing import Annotated, Dict, Literal, Callable
from typing_extensions import TypedDict
from langgraph.graph import add_messages
from langgraph.graph.message import AnyMessage


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    current_assistant: Literal[
        'primary_assistant',
        'order_assistant',
        'menu_assistant',
    ]
