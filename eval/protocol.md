# Eval protocol — provenance vs plain chat

## Цель

Сравнить не «красоту текста», а **проверяемость**: доля утверждений со ссылкой на open source / claim.

## Выборка (МегаКино)

10 утверждений из `projects/demo-megakino/report.md` / strategies (смесь fact/hypothesis/forecast).

## Скоры

| Метод | Provenance score | Примечание |
|-------|------------------|----------|
| Agent (этот репо) | доля утверждений с claim/evidence id | |
| Plain chat (оценка) | обычно низкая без принуждения к источникам | |
| Manual analyst | высокая при доступе к тем же open URL | время выше |

## Проведение

1. Выписать 10 утверждений.
2. Для каждого: есть ли явный source/claim? (да=1/нет=0)
3. Записать в `results.md`.
