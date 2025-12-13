# llm_agent.py
import json
from openai import OpenAI
from config import OPENAI_API_KEY

# --- Outils pour le LLM ---
def get_best_csp_suggestions(solver, k=5):
    return solver.suggest()[:k]

def choose_word(word: str):
    return {"chosen_word": word}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_best_csp_suggestions",
            "description": "Get the best candidate words from the CSP Wordle solver",
            "parameters": {
                "type": "object",
                "properties": {
                    "k": {"type": "integer", "description": "Number of candidate words to retrieve"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "choose_word",
            "description": "Select the final word to guess in Wordle",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {"type": "string"}
                },
                "required": ["word"]
            }
        }
    }
]

def llm_choose_next_guess(solver, previous_steps):
    # 🔹 Crée le client ici pour éviter les problèmes de thread/global
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = """
You are a Wordle-solving agent.

Rules:
- You must use CSP solver suggestions.
- You must choose exactly one valid 5-letter word.
- Your goal is to minimize the expected number of remaining candidates.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""
Previous guesses:
{previous_steps}

Remaining candidates: {len(solver.candidates)}

Decide the next best guess.
"""}
    ]

    # --- Appel au LLM ---
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=tools,
        function_call="auto",
        temperature=0
    )

    msg = response.choices[0].message

    # --- Gestion des tool calls ---
    if getattr(msg, "tool_calls", None):
        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)

            if name == "get_best_csp_suggestions":
                return get_best_csp_suggestions(solver, **args)

            if name == "choose_word":
                return args["word"]

    # --- Fallback: CSP-only ---
    return solver.suggest()[0]
