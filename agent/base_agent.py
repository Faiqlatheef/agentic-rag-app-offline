from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def run(self, query: str) -> str:
        pass

    @abstractmethod
    def get_context(self, query: str) -> str:
        pass
