from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def choose_next_guess(self, solver, steps) -> str:
        pass
