from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate
from prompts import IDENTITY, ADDITIONAL_GUARDRAILS


menu_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', "Your role is to respond to customer queries related to the menu, ingredients, or other food-related topics. " \
             "If the user requests assistance beyond the scope of your tools, escalate the conversation using 'CompleteOrEscalate.' "
             + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

menu_assistant_tools = [fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate]
