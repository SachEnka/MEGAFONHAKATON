# Безопасность — локальный режим (Ollama)

## Принципы

1. **Инференс локально** — модель через Ollama на `127.0.0.1:11434`; облачные API-ключи для базового запуска не нужны.
2. **Данные проекта на диске** — evidence/state/outputs только в репозитории; сессии пишутся в `projects/<id>/state/local_sessions/`.
3. **Секреты не в git** — `.env` в `.gitignore`; в репо только `.env.example`.
4. **Sandbox путей** — `read/write/list/grep` только внутри корня репозитория; запись в `.env` / `.git` / `secrets/` запрещена.
5. **SSRF-защита web_fetch** — только `http/https`, блок localhost/private IP; опциональный allowlist суффиксов (`WEB_ALLOW_SUFFIXES`).
6. **Allowlist CLI** — агент не получает произвольный shell; только `tools/*.py` из белого списка.
7. **Human gate** — `ask_user` для существенного выбора (варианты стратегии).
8. **Инструкции из источников** — не переопределяют `AGENTS.md` (закреплено в system prompt).

## Что не делает локальный агент

- Не отправляет бриф/evidence на сторонние LLM API (если вы сами не смените `OLLAMA_HOST` на облако).
- Не хранит ключи МегаФона — их и не должно быть: только open data.
- Не является необузданным RCE: shell вне allowlist недоступен.

## Рекомендуемая конфигурация

```env
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3:8b
ALLOW_WEB_FETCH=1
WEB_ALLOW_SUFFIXES=megafon.ru,wikipedia.org,github.com,habr.com
```

Для полностью офлайн-прогона (только файлы репо): `ALLOW_WEB_FETCH=0`.

## Паттерны open-source

Устройство loop + tools взято из практики локальных агентов (Ollama tool calling, [local-cli](https://github.com/lutelute/local-cli), примеры [ollama-python](https://github.com/ollama/ollama-python)): модель предлагает tool call → runtime исполняет в sandbox → результат обратно в контекст.
