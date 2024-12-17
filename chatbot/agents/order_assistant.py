from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_full_menu, fetch_order, place_on_site_order, place_pickup_order, place_delivery_order, CompleteOrEscalate
from prompts import IDENTITY, ADDITIONAL_GUARDRAILS


order_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', "Your role is to assist customers in placing orders based on their requests. " \
             "You are responsible for gathering the necessary order information and using the available tools to process the order. " \
             "If the user requests assistance beyond the scope of your role, responsibilities, or available tools, " \
             "you should call 'CompleteOrEscalate' to escalate the conversation for further handling. "
             + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

order_assistant_tools = [fetch_full_menu, fetch_order, place_on_site_order, place_pickup_order, place_delivery_order, CompleteOrEscalate]
