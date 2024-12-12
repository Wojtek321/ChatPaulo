from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate
from prompts import IDENTITY, ADDITIONAL_GUARDRAILS


menu_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', "Utilize the available tools to accurately address user inquiries regarding the menu, ingredients, pizzas, or any other food-related topics." \
             "If the user requests assistance beyond the scope of these tools, escalate the conversation using 'CompleteOrEscalate.' " \
             "Focus on providing clear and concise responses without unnecessary delays. Avoid inventing non-existent tools or functionalities"),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

menu_assistant_tools = [fetch_full_menu, fetch_item_ingredients, fetch_ingredient_list, fetch_ingredient, fetch_pizza_details, CompleteOrEscalate]
