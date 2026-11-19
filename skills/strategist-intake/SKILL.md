---
name: strategist-intake
description: >-
  Уточняет размытый запрос руководителя продукта до исполнимой задачи:
  решение, получатель, ограничения, данные. Использовать в начале проекта
  или когда CURRENT.md отсутствует / фаза intake.
---

# Skill: Intake

1. Прочитай `AGENTS.md` и `knowledge/methods/intake.md`.
2. Если есть `projects/<id>/brief.md` — извлеки уже сказанное; не переспрашивай.
3. Задай только блокирующие вопросы (если нужны).
4. Создай/обнови:
   - `projects/<id>/brief.md` (уточнённая версия)
   - `projects/<id>/state/CURRENT.md` из `templates/CURRENT.md`
   - начни `state/ledger.md`
5. Переведи фазу в `gather`, запиши Next action.
6. `python tools/cost_log.py <id> --note "intake"` при возможности.
