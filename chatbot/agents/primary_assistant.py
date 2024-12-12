from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_pizzeria_info, ToMenuAssistant, ToOrderAssistant
from prompts import IDENTITY, ADDITIONAL_GUARDRAILS


primary_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', "Your role is to warmly welcome customers. " \
             "You are responsible for answering customer inquiries regarding the pizzeria. "
             "If the customer needs help with menu-related inquiries or placing an order, you should use the relevant tool."
             + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

primary_assistant_tools = [fetch_pizzeria_info, ToMenuAssistant, ToOrderAssistant]
