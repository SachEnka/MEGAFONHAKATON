---
name: gather-evidence
description: >-
  Собирает материалы из inputs, таблиц и разрешённых сайтов; сохраняет
  evidence со ссылками и claims. Фаза gather.
---

# Skill: Gather evidence

1. Прочитай brief + `knowledge/methods/evidence.md` + `claims.md`.
2. Инвентаризируй `inputs/`; выпиши список URL/файлов в ledger.
3. Для каждого существенного источника создай `evidence/YYYYMMDD-slug.md`.
4. Добавь claims в `state/claims.jsonl` (`fact` только из источника).
5. При таблицах — `python tools/analyze_table.py <csv>`.
6. Обнови индекс: `python tools/evidence_index.py <id>`.
7. CURRENT.md → phase `research`, next = situation synthesis.
8. Сбои источников — по `knowledge/antifragile/resilience.md`.
