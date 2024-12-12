from langchain_core.runnables import Runnable
from state import State


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State):
        result = self.runnable.invoke(state)

        return {'messages': result}