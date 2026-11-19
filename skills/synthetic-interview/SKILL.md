---
name: synthetic-interview
description: >-
  Готовит гайд интервью и/или проводит беседу с ИИ-респондентом в роли.
  Синтетика только для гипотез; никогда не доказывает спрос.
---

# Skill: Synthetic interview

## Важно

Ответы модельного респондента = **гипотезы**. Нельзя писать «пользователи хотят X» как fact. В evidence и claims: `synthetic: true`, type `hypothesis`.

## Шаги

1. Сформулируй роль (сегмент, ситуация, ограничения) и цель гипотез.
2. Подготовь гайд (5–10 вопросов, без наводок).
3. Проведи диалог (субагент `respondent-*` или в этом чате с явной ролью).
4. Сохрани `evidence/YYYYMMDD-synthetic-<role>.md`:

```markdown
# SYNTHETIC INTERVIEW — не доказательство спроса
- Role: …
- Purpose: hypothesis generation only
…
```

5. Извлеки гипотезы в claims.jsonl с `"synthetic": true`.
6. Реальные интервью — только с согласием; в репо без ПДн.
