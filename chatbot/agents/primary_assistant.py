from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_pizzeria_info, MenuInfoTool, OrderManagementTool
from prompts import PRIMARY_PROMPT, PRIMARY_INFORMATION, PRIMARY_EXAMPLES, IDENTITY, ADDITIONAL_GUARDRAILS
from .assistant import Assistant, llm


primary_assistant_prompt = ChatPromptTemplate([
    ('system', IDENTITY),
    ('user', PRIMARY_PROMPT
           + PRIMARY_INFORMATION
           + PRIMARY_EXAMPLES
           + ADDITIONAL_GUARDRAILS),
    ('assistant', "Understood"),
    ('placeholder', '{messages}'),
])

primary_assistant_tools = [fetch_pizzeria_info, MenuInfoTool, OrderManagementTool]

assistant_runnable = primary_assistant_prompt | llm.bind_tools(primary_assistant_tools)

primary_assistant = Assistant(assistant_runnable)
