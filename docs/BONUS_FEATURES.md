# Дополнительный уровень — что реализовано и зачем

Каждый пункт оправдан пользой для качества, скорости, стоимости или сопровождения.

| Возможность | Где | Польза |
|-------------|-----|--------|
| Синтетические интервью | `skills/synthetic-interview`, evidence `*-synthetic-*` | Быстрые гипотезы барьеров; явная маркировка ≠ спрос |
| UX разбор интерфейса | `skills/ux-interface-review`, `evidence/20261104-ux-landing.md` | Барьер понимания привязан к видимому на лендинге |
| Анализ данных | `tools/analyze_table.py` + CSV inputs | Воспроизводимые расчёты, проверка пропусков/единиц |
| Media review | `skills/media-review` | Скрины/изображения; ASR — только по текстовой расшифровке |
| Impact / revise | `tools/impact.py`, `revision_log` | Какие выводы держатся на claim/source |
| Eval provenance | `eval/results.md` | Сравнение с plain chat / manual |
| Поддержка решений | `skills/decision-support`, `state/decisions.md` | Обязательства, KPI, условия пересмотра |
| Пересмотр при новых данных | `skills/revise-on-new-data` | Точечное обновление claims/outputs |
| Routing | `knowledge/routing/` | Экономия: cheap vs deep, исправление ошибочного выбора |
| Skills | `skills/*` | Повторяемые процедуры фаз |
| Hooks | `.cursor/hooks.json` | Не забывать ledger/cost |
| Субагенты | `knowledge/routing/subagents.md` | Изоляция задач, меньше раздувания контекста |
| Agency Agents | `.cursor/rules/*` из [agency-agents](https://github.com/msitarzewski/agency-agents) | Готовые специалисты product/UX/research/comms под фазы Стратега |
| MCP + CLI | Browser MCP + `tools/` + **`python -m local_agent` (Ollama)** | Локальный loop без облачных ключей; allowlist tools |
| Локальная безопасность | `docs/SECURITY.md`, sandbox/SSRF | Соответствие требованию «секреты не в репо», данные на машине |
| База знаний | `knowledge/INDEX.md` + методы | Навигация по смыслу/связям; память сеансов отдельно |
| Устойчивость | `knowledge/antifragile/resilience.md` | Сбои заметны; нет тихих повторов |
| Переносимость | файловый state | Другая машина/чат = resume |
| Сравнение с baseline | `tools/compare_baseline.py`, `outputs/baseline_comparison.md` | Прозрачность времени/стоимости vs ручной / plain chat |

## Не реализовывали (см. LIMITATIONS)

Векторный поиск по базе знаний, полноценные аудио/видео пайплайны, отдельный рантайм-оркестратор — низкий ROI относительно обязательного минимума и удобства в Cursor.
