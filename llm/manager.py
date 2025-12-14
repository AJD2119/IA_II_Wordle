from .heuristic_llm import HeuristicLLM
from .openai_llm import OpenAILLM
from .ollama_llm import OllamaLLM
from .gemini_llm import GeminiLLM

class LLMManager:
    def __init__(self, llm_type="heuristic"):
        self.llm_type = llm_type
        self.llm = self._init_llm(llm_type)

    def _init_llm(self, llm_type):
        if llm_type == "openai":
            return OpenAILLM()
        if llm_type == "ollama":
            return OllamaLLM()
        if llm_type == "gemini":
            return GeminiLLM()
        return HeuristicLLM()

    def choose_next_guess(self, solver, steps):
        return self.llm.choose_next_guess(solver, steps)
