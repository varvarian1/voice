import requests

from config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT, WEB_SEARCH_MAX_RESULTS
from search.duckduckgo import web_search

SEARCH_PREFIX = "SEARCH:"

SYSTEM_PROMPT = (
    "Ты — голосовой ассистент. Отвечай кратко, по делу, на русском языке. "
    "Если ты не знаешь ответа или не уверен в нём, не выдумывай факты — "
    f"ответь ТОЛЬКО одной строкой в формате '{SEARCH_PREFIX} <поисковый запрос>', без пояснений."
)

FOLLOWUP_SYSTEM_PROMPT = (
    "Ты — голосовой ассистент. Тебе даны результаты веб-поиска и вопрос пользователя. "
    "Ответь на вопрос кратко и по делу на русском языке, основываясь на результатах поиска. "
    "Не используй маркер SEARCH снова — просто дай финальный ответ."
)


class OllamaClient:
    def __init__(self, host=OLLAMA_HOST, model=OLLAMA_MODEL):
        self.host = host.rstrip("/")
        self.model = model

    def _generate(self, prompt: str, system: str) -> str:
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "system": system,
                "stream": False,
            },
            timeout=OLLAMA_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    def ask(self, prompt: str) -> str | None:
        try:
            answer = self._generate(prompt, SYSTEM_PROMPT)
        except requests.exceptions.RequestException as e:
            print(f"Ollama request failed: {e}")
            return None

        if not answer.upper().startswith(SEARCH_PREFIX):
            return answer

        query = answer[len(SEARCH_PREFIX):].strip()
        search_results = web_search(query, max_results=WEB_SEARCH_MAX_RESULTS)

        if not search_results:
            return "Не удалось найти информацию по этому запросу."

        followup_prompt = (
            f"Вопрос пользователя: {prompt}\n\n"
            f"Результаты поиска по запросу '{query}':\n{search_results}"
        )

        try:
            return self._generate(followup_prompt, FOLLOWUP_SYSTEM_PROMPT)
        except requests.exceptions.RequestException as e:
            print(f"Ollama request failed: {e}")
            return None
