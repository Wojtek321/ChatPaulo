from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image
from dotenv import load_dotenv

from state import State, create_entry_node, to_primary_assistant
from tools import CompleteOrEscalate, MenuInfoTool, OrderManagementTool
from agents import primary_assistant_prompt, primary_assistant_tools, menu_assistant_prompt, menu_assistant_tools, order_assistant_prompt, order_assistant_tools, Assistant

load_dotenv()


# llm = ChatOpenAI(model='gpt-4o')
llm = ChatAnthropic(model='claude-3-5-haiku-latest')

workflow = StateGraph(State)


def route_to_active_assistant(state: State):
    """Routes user input to current active assistant."""
    current_assistant = state.get('current_assistant')
    if not current_assistant:
        return 'primary_assistant'
    return current_assistant


workflow.add_conditional_edges(START, route_to_active_assistant, ['primary_assistant', 'menu_assistant', 'order_assistant'])


# primary assistant
assistant_runnable = primary_assistant_prompt | llm.bind_tools(primary_assistant_tools)

workflow.add_node('primary_assistant', Assistant(assistant_runnable))
workflow.add_node('primary_tools', ToolNode(primary_assistant_tools))


def route_primary_assistant(state: State):
    route = tools_condition(state)
    if route == END:
        return END

    tool_calls = state['messages'][-1].tool_calls
    if tool_calls:
        tool_name = tool_calls[0]['name']
        if tool_name == MenuInfoTool.__name__:
            return 'enter_menu'
        elif tool_name == OrderManagementTool.__name__:
            return 'enter_order'
        return 'primary_tools'

    raise ValueError('Invalid route.')


workflow.add_conditional_edges('primary_assistant', route_primary_assistant, ['enter_menu', 'enter_order', 'primary_tools', END])
workflow.add_edge('primary_tools', 'primary_assistant')


# menu assistant
menu_assistant_runnable = menu_assistant_prompt | llm.bind_tools(menu_assistant_tools)

workflow.add_node('enter_menu', create_entry_node('Menu Assistant', 'menu_assistant'))
workflow.add_node('menu_assistant', Assistant(menu_assistant_runnable))
workflow.add_edge('enter_menu', 'menu_assistant')
workflow.add_node('menu_tools', ToolNode(menu_assistant_tools))


def route_menu_assistant(state: State):
    route = tools_condition(state)
    if route == END:
        return END

    tool_calls = state['messages'][-1].tool_calls
    if any(tc['name'] == CompleteOrEscalate.__name__ for tc in tool_calls):
        return 'return_to_primary'

    return 'menu_tools'


workflow.add_conditional_edges('menu_assistant', route_menu_assistant, ['menu_tools', 'return_to_primary', END])
workflow.add_edge('menu_tools', 'menu_assistant')


# order assistant
order_assistant_runnable = order_assistant_prompt | llm.bind_tools(order_assistant_tools)

workflow.add_node('enter_order', create_entry_node('Order Placing Assistant', 'order_assistant'))
workflow.add_node('order_assistant', Assistant(order_assistant_runnable))
workflow.add_edge('enter_order', 'order_assistant')
workflow.add_node('order_tools', ToolNode(order_assistant_tools))


def route_order_assistant(state: State):
    route = tools_condition(state)
    if route == END:
        return END

    tool_calls = state['messages'][-1].tool_calls
    if any(tc['name'] == CompleteOrEscalate.__name__ for tc in tool_calls):
        return 'return_to_primary'

    return 'order_tools'


workflow.add_conditional_edges('order_assistant', route_order_assistant, ['order_tools', 'return_to_primary', END])
workflow.add_edge('order_tools', 'order_assistant')


# back to primary assistant
workflow.add_node('return_to_primary', to_primary_assistant)
workflow.add_edge('return_to_primary', 'primary_assistant')


memory = MemorySaver()

graph = workflow.compile(
    checkpointer=memory,
)


if __name__ == '__main__':
    try:
        img = Image(graph.get_graph(xray=True).draw_mermaid_png())
        with open('../assets/graph_workflow.png', 'wb') as f:
            f.write(img.data)
    except Exception:
        pass
