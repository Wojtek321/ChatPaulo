from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_full_menu, fetch_order, place_on_site_order, place_pickup_order, place_delivery_order, CompleteOrEscalate
from prompts import IDENTITY, ADDITIONAL_GUARDRAILS


order_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', "Use are responsible for placing orders according to customers' requests. " \
             "Your job is to collect required order information and create order using provided functions. " \
             "If the user needs help, and none of your tools are appropriate for it, then 'CompleteOrEscalate' the dialog. " \
             + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

order_assistant_tools = [fetch_full_menu, fetch_order, place_on_site_order, place_pickup_order, place_delivery_order, CompleteOrEscalate]
