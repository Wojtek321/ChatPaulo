from typing import Annotated, Dict, Literal, Callable
from typing_extensions import TypedDict
from langgraph.graph import add_messages
from langgraph.graph.message import AnyMessage
from langchain_core.messages import ToolMessage


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    current_assistant: Literal[
        'primary_assistant',
        'order_assistant',
        'menu_assistant',
    ]


def to_primary_assistant(state: State) -> Dict:
    """Resets current assistant to the primary assistant"""
    messages = []
    last_message = state['messages'][-1]

    if last_message.tool_calls:
        messages.append(
            ToolMessage(
                content="Returning control to primary assistant. Please reflect on the past conversation and assist the user as needed.",
                tool_call_id=last_message.tool_calls[0]['id']
            )
        )

    return {
        'current_assistant': None,
        'messages': messages
    }


def create_entry_node(assistant_name: str, new_assistant: str) -> Callable:
    """Creates an entry point for a specific assistant."""
    def entry_node(state: State) -> Dict:
        tool_call_id = state['messages'][-1].tool_calls[0]['id']
        return {
            'messages': [
                ToolMessage(
                    content=f"The system has switched to the {assistant_name}. Reflect on the above conversation between the host assistant and the user. "
                            "The user's intent is unsatisfied. Utilize the provided tools to address the user's request effectively. "
                            "If the user changes their intent or needs help for other tasks, call the CompleteOrEscalate to let the primary host assistant take control. "
                            "Maintain focus on resolving the user's needs without explicitly identifying your role.",
                    tool_call_id=tool_call_id,
                )
            ],
            "current_assistant": new_assistant
        }

    return entry_node
