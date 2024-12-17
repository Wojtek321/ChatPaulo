from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate
from prompts import IDENTITY, ADDITIONAL_GUARDRAILS


menu_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', "Your role is to answer customer questions about the menu, ingredients, or any other food-related topics. " \
             "You are expected to use the provided tools to assist customers effectively. " \
             "If the user requests assistance beyond the scope of your role, responsibilities, or available tools, " \
             "you should call 'CompleteOrEscalate' to escalate the conversation for further handling. "
             + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

menu_assistant_tools = [fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate]
