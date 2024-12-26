from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from state import State


# Base class for creating assistants
class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State):
        result = self.runnable.invoke(state)

        return {'messages': result}


# Choose the LLM to be used
llm = ChatOpenAI(model='gpt-4o')
# llm = ChatAnthropic(model='claude-3-5-sonnet-latest')