# Модуль 2. Prompt Injection и Security Testing

## Цель

Системно проверять устойчивость AI-ботов к атакам и утечкам.

## Уроки

- Prompt injection: direct, jailbreak, indirect
- Red teaming: payload splitting, encoding, context flooding, escalation
- Guardrails: input/output фильтрация, false positives
- Consistency и bias testing
- Regression testing для промптов
- CI/CD для AI-тестов

## Файлы

```
source_materials/
  day8_prompt_injection.py
  day9_red_teaming.py
  day10_guardrails.py
  day11_consistency_bias.py
  day12_regression_testing.py
  day13_ci_cd.py
projects/
  project2_robustness_suite/
```

## Запуск

```bash
python source_materials/day8_prompt_injection.py
python source_materials/day10_guardrails.py
python source_materials/day12_regression_testing.py
python projects/project2_robustness_suite/run_suite.py
```

## Домашнее задание

Создайте 20 атак, сгруппируйте по типам и оформите 3 security bug reports.
