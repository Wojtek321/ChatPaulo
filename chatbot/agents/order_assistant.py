from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_full_menu, fetch_order, place_on_site_order, place_pickup_order, place_delivery_order, CompleteOrEscalate, cancel_order, update_order
from prompts import ORDER_PROMPT, ORDER_INSTRUCTIONS, IDENTITY, ADDITIONAL_GUARDRAILS
from .assistant import Assistant, llm


order_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', ORDER_PROMPT
           + ORDER_INSTRUCTIONS
           + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

order_assistant_tools = [fetch_full_menu, fetch_order, place_on_site_order, place_pickup_order, place_delivery_order, cancel_order, update_order, CompleteOrEscalate]

order_assistant_runnable = order_assistant_prompt | llm.bind_tools(order_assistant_tools)

order_assistant = Assistant(order_assistant_runnable)
