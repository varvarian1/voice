# TODO

## Сделано
- [x] `docker-compose.yml`: сервис `python-app` собирается из существующего `Dockerfile`, без ручной установки зависимостей. Работает "как есть" на Windows/WSL для сборки и smoke-теста (без реального микрофона).
- [x] `docker-compose.audio.yml`: override-файл с проброс `/dev/snd` и группы `audio` — применяется только там, где устройство реально существует (Linux-сервер с звуковой картой): `docker compose -f docker-compose.yml -f docker-compose.audio.yml up -d`.
- [x] Проверено локально: `docker compose up --build` на Windows собирает образ и стартует контейнер без ошибок конфига; приложение падает на этапе открытия микрофона (`OSError: Invalid input device`) — ожидаемо, т.к. на Windows/Docker Desktop нет доступного `/dev/snd` (даже через WSL2 — проверено, устройства нет и в дистрибутиве `docker-desktop`).

## Отложено (пока не делаем)
- [ ] Сервис `ollama` в docker-compose (образ `ollama/ollama`, автоскачка модели `gemma4:e4b`) — вернёмся к этому после того, как доделаем Python-часть.

## Дальше (Python-часть, без Docker)
- [ ] `src/llm/ollama_client.py`: клиент для запроса к Ollama (`/api/generate`) с моделью `gemma4:e4b`.
- [ ] `src/config.py`: добавить чтение `OLLAMA_HOST` / `OLLAMA_MODEL` из окружения.
- [ ] `src/main.py`: после распознавания команды (`Command: ...`) отправлять текст в LLM и выводить ответ в консоль.
- [ ] Озвучка ответа LLM через TTS (позже, не сейчас).

## Заметки
- Реальный тест с микрофоном возможен только на целевом Linux-сервере (или Linux-хосте с нативным Docker) — на Windows/Docker Desktop проброс аудио-устройств в контейнер не поддерживается в принципе, это ограничение платформы.
