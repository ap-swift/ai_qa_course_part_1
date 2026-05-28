# Проект 2. AI Security & Robustness Suite

End-to-end набор проверок безопасности и устойчивости AI customer support assistant.

## Категории тестов

| Категория | Количество | Назначение |
|---|---:|---|
| Normal Functionality | 20 | Проверить обычные пользовательские сценарии. |
| Injection Attacks | 15 | Проверить устойчивость к prompt injection. |
| Consistency | 10 | Проверить стабильность поведения на повторных запросах. |

Всего: 45 test cases.

## Архитектура

```text
User Input -> [Input Guardrail] -> LLM -> [Output Guardrail] -> Response
                 |                         |
              BLOCK if                  BLOCK if
              suspicious                leaks info
```

## Запуск

```bash
python 02_prompt_injection_and_security/projects/project2_robustness_suite/run_suite.py
pytest 02_prompt_injection_and_security/projects/project2_robustness_suite/ -v
```

## CI/CD

Для CI используйте GitHub Secrets или другой защищенный механизм хранения ключей. Не вставляйте ключи в YAML, README, поля Stepik или screenshots.

## Методика

1. Normal tests: проверка функциональных требований.
2. Injection tests: attack vectors по OWASP LLM Top 10.
3. Consistency tests: сравнение стабильности ответов на повторных запусках.

## Что описать в отчете

1. Какие типы атак оказались наиболее эффективными?
2. Какой false positive rate у guardrails?
3. Насколько стабильны ответы на objective и subjective вопросы?
