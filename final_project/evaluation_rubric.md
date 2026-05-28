# Evaluation Rubric: 100 баллов

## 1. Структура проекта — 10 баллов
- 0-3: файлы разрознены, запуск непонятен.
- 4-7: структура в целом понятна, но есть пробелы в README или данных.
- 8-10: чистая структура, понятные папки, `.env.example`, команды запуска.

## 2. Качество test cases — 20 баллов
- 0-7: мало кейсов, нет expected results.
- 8-14: есть разные категории, но критерии частично субъективны.
- 15-20: 20+ кейсов, четкие expected results, edge cases и regression logic.

## 3. Security testing — 15 баллов
- 0-5: security почти не покрыт.
- 6-10: есть prompt injection и jailbreak cases, но мало классификации.
- 11-15: attack catalog, pass/fail критерии, false positives, ethical scope.

## 4. Automation — 15 баллов
- 0-5: проверки запускаются вручную без структуры.
- 6-10: есть pytest/promptfoo, но запуск частично нестабилен.
- 11-15: воспроизводимый suite, markers, fixtures, понятные failures.

## 5. RAG/LLM evaluation — 15 баллов
- 0-5: качество ответов оценивается субъективно.
- 6-10: есть базовые checks для hallucinations или retrieval.
- 11-15: retrieval и generation разделены, есть метрики и интерпретация.

## 6. Отчетность — 10 баллов
- 0-3: нет выводов или evidence.
- 4-7: есть summary, но мало impact/recommendations.
- 8-10: defects, severity, evidence, risks и actionable recommendations.

## 7. Воспроизводимость — 10 баллов
- 0-3: проект нельзя запустить без автора.
- 4-7: запуск возможен, но есть скрытые шаги.
- 8-10: clean setup, requirements, `.env.example`, test data, expected commands.

## 8. Оформление GitHub — 5 баллов
- 0-2: README слабый или отсутствует.
- 3-4: README есть, но не хватает контекста или результатов.
- 5: профессиональное портфолио-оформление без секретов и приватных данных.
