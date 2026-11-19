---
name: strategy-pack
description: >-
  После выбора человеком пишет согласованные product_strategy,
  communication_strategy и validation_plan.
---

# Skill: Strategy pack

**Предусловие:** выбор варианта зафиксирован в CURRENT.md / decisions.

1. Методы: product_strategy, communication_strategy, validation.
2. Сначала `outputs/product_strategy.md`.
3. Затем `outputs/communication_strategy.md` (обещания ⊆ продукт). Субагент `comms` допустим.
4. Затем `outputs/validation_plan.md`.
5. `python tools/validate_artifacts.py <id>`.
6. CURRENT → `after` или `done` после decision-support.
