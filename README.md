##Автоматизированные тесты для PetStore API с использованием Pydantic и Allure.

## Установка

1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. (Опционально) Создайте файл `.env` для настройки:
```
BASE_URL=https://petstore.swagger.io/v2
API_KEY=your_api_key_here
```

## Запуск тестов

### Базовый запуск
```bash
cd petstore_api_tests
pytest tests/
```

### С генерацией Allure отчетов
```bash
cd petstore_api_tests
pytest --alluredir=allure-results tests/
allure serve allure-results
```

**Примечание:** Для просмотра Allure отчетов необходимо установить Allure командную строку:
- Mac: `brew install allure`

### Запуск конкретного теста
```bash
cd petstore_api_tests
pytest tests/test_pet_crud.py::TestPetCRUD::test_create_pet
```

### Запуск с подробным выводом
```bash
cd petstore_api_tests
pytest tests/ -v
```

## Тесты

Проект включает тесты для:
- Создание питомца (POST /pet)
- Получение питомца по ID (GET /pet/{petId})
- Обновление питомца (PUT /pet)
- Удаление питомца (DELETE /pet/{petId})
- Поиск питомцев по статусу (GET /pet/findByStatus)
- Валидация обязательных полей

