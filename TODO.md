# TODO

## Сделано
- [x] `docker-compose.yml`: сервис `app` собирается из существующего `Dockerfile`, без ручной установки зависимостей.
- [x] Проброс `/dev/snd` и группы `audio` в контейнер `app` для доступа к микрофону на Linux-сервере.

## Отложено (пока не делаем)
- [ ] Сервис `ollama` в docker-compose (образ `ollama/ollama`, автоскачка модели `gemma4:e4b`) — вернёмся к этому после того, как доделаем Python-часть.

## Дальше (Python-часть, без Docker)
- [ ] `src/llm/ollama_client.py`: клиент для запроса к Ollama (`/api/generate`) с моделью `gemma4:e4b`.
- [ ] `src/config.py`: добавить чтение `OLLAMA_HOST` / `OLLAMA_MODEL` из окружения.
- [ ] `src/main.py`: после распознавания команды (`Command: ...`) отправлять текст в LLM и выводить ответ в консоль.
- [ ] Озвучка ответа LLM через TTS (позже, не сейчас).
