from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate
from prompts import MENU_PROMPT, IDENTITY, ADDITIONAL_GUARDRAILS
from .assistant import Assistant, llm


menu_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', MENU_PROMPT
           + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

menu_assistant_tools = [fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate]

menu_assistant_runnable = menu_assistant_prompt | llm.bind_tools(menu_assistant_tools)

menu_assistant = Assistant(menu_assistant_runnable)
