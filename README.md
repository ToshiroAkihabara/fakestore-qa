# fakestore-qa

Автоматизация API- и UI-тестов
для React-витрины в Docker, работающей на базе
[fakestoreapi.com](https://fakestoreapi.com).

## Технологический стек

| Инструмент | Назначение |
|---|---|
| behave | API-тесты в стиле BDD |
| Playwright + pytest | UI-тесты с использованием паттерна Page Object Model |
| Allure | Единая отчетность для обоих наборов тестов |
| Docker Compose | Локальный запуск витрины |
| GitHub Actions | CI и публикация отчетов |

## Структура проекта

```text
api_tests/     # BDD-тесты behave для REST API endpoints
ui_tests/      # page objects и тесты на pytest + Playwright
storefront/    # Dockerized React-приложение под тестированием
docs/          # тест-план, ручные кейсы и руководство по проекту
```

## Локальный запуск

**Предварительные требования:** Python 3.11, Docker

```bash
pip install -r requirements.txt
playwright install chromium

# API-тесты
behave api_tests/features/ --format pretty

# Запуск витрины
docker compose up -d --build --wait

# UI-тесты
pytest ui_tests/tests/ -v

# Остановка витрины
docker compose down
```

## Отчеты

- Локальные результаты Allure: `allure serve allure-results/`
- CI публикует отчет Allure из ветки `gh-pages` после push в `main`
