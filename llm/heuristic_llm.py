from .base import BaseLLM

class HeuristicLLM(BaseLLM):
    def choose_next_guess(self, solver, steps):
        return solver.suggest()[0]
