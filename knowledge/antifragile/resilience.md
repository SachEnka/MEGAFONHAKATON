# Устойчивость к сбоям

## Принципы

1. **Замечай** — ошибка инструмента/сети пишется в `ledger.md`, не глотается.
2. **Не повторяй незаметно** — перед повторным сбором проверь, есть ли уже evidence с тем же source.
3. **Продолжай с пробелом** — недоступный источник = gap в situation, не выдумка.
4. **Идемпотентность** — повторный запуск фазы дописывает ledger («revisit»), не затирает историю.
5. **Переносимость** — весь прогресс в файлах проекта; новый чат / другая машина = читать `CURRENT.md`.

## Шаблон записи сбоя

```markdown
### YYYY-MM-DD HH:MM — tool_failure
- Tool: browser / analyze_table / ...
- Target: URL or path
- Error: ...
- Action: skip | retry_once | alternate_source
- Artifact impact: none | partial evidence E...
```
