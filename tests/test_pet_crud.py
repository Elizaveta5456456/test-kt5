import pytest
import allure
from petstore_api_tests.client.pets_client import PetsClient
from petstore_api_tests.models.pet import Pet, UpdatePet


@allure.epic("PetStore API")
@allure.feature("Pet CRUD Operations")
class TestPetCRUD:
    """Тесты для CRUD операций с питомцами"""
    
    @allure.story("Create Pet")
    @allure.title("Создание нового питомца")
    @allure.description("Проверка создания питомца с валидацией статус-кода, тела ответа и JSON-схемы")
    def test_create_pet(self, class_pets_client: PetsClient, pet_data: Pet):
        """Тест создания нового питомца"""
        with allure.step("Подготовка данных для создания питомца"):
            pet = pet_data
        
        with allure.step("Отправка POST запроса для создания питомца"):
            response = class_pets_client.create_pet(pet)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code in [200, 201], \
                f"Ожидался статус 200 или 201, получен {response.status_code}. Ответ: {response.text}"
        
        with allure.step("Валидация JSON-схемы ответа через Pydantic"):
            response_pet = Pet(**response.json())
            assert response_pet.id is not None, "ID питомца не должен быть None"
            assert response_pet.name == pet.name, "Имя питомца не совпадает"
            assert response_pet.status == pet.status, "Статус питомца не совпадает"
        
        with allure.step("Проверка сохранения всех атрибутов"):
            response_dict = response_pet.model_dump(by_alias=True, exclude_none=True)
            original_dict = pet.model_dump(by_alias=True, exclude_none=True)
            # Сравниваем основные поля (исключая id, который генерируется сервером)
            assert response_dict.get("name") == original_dict.get("name")
            assert response_dict.get("status") == original_dict.get("status")
    
    @allure.story("Read Pet")
    @allure.title("Получение питомца по ID")
    @allure.description("Проверка получения питомца с валидацией статус-кода и JSON-схемы")
    def test_get_pet_by_id(self, class_pets_client: PetsClient, function_pet: int):
        """Тест получения питомца по ID"""
        pet_id = function_pet
        
        with allure.step(f"Отправка GET запроса для получения питомца с ID {pet_id}"):
            response = class_pets_client.get_pet_by_id(pet_id)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        with allure.step("Валидация JSON-схемы ответа через Pydantic"):
            response_pet = Pet(**response.json())
            assert response_pet.id == pet_id, f"ID питомца должен быть {pet_id}"
            assert response_pet.name is not None, "Имя питомца не должно быть None"
    
    @allure.story("Update Pet")
    @allure.title("Обновление питомца")
    @allure.description("Проверка обновления питомца с валидацией статус-кода и сохранения данных")
    def test_update_pet(self, class_pets_client: PetsClient, function_pet: int):
        """Тест обновления питомца"""
        pet_id = function_pet
        
        with allure.step("Подготовка данных для обновления"):
            # Получаем текущего питомца
            get_response = class_pets_client.get_pet_by_id(pet_id)
            current_pet = Pet(**get_response.json())
            
            # Создаем обновленные данные
            updated_pet = Pet(
                id=pet_id,
                name="Updated Pet Name",
                status="sold",
                category=current_pet.category,
                photo_urls=current_pet.photo_urls,
                tags=current_pet.tags
            )
        
        with allure.step("Отправка PUT запроса для обновления питомца"):
            response = class_pets_client.update_pet(updated_pet)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        with allure.step("Валидация обновленных данных"):
            response_pet = Pet(**response.json())
            assert response_pet.id == pet_id, f"ID питомца должен быть {pet_id}"
            assert response_pet.name == "Updated Pet Name", "Имя питомца должно быть обновлено"
            assert response_pet.status == "sold", "Статус питомца должен быть обновлен"
    
    @allure.story("Delete Pet")
    @allure.title("Удаление питомца")
    @allure.description("Проверка удаления питомца с валидацией статус-кода")
    def test_delete_pet(self, class_pets_client: PetsClient):
        """Тест удаления питомца"""
        with allure.step("Создание питомца для удаления"):
            pet = Pet()
            create_response = class_pets_client.create_pet(pet)
            assert create_response.status_code in [200, 201]
            pet_id = create_response.json().get("id") or pet.id
        
        with allure.step(f"Отправка DELETE запроса для удаления питомца с ID {pet_id}"):
            response = class_pets_client.delete_pet(pet_id)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        with allure.step("Проверка, что питомец действительно удален"):
            get_response = class_pets_client.get_pet_by_id(pet_id)
            assert get_response.status_code == 404, \
                f"Питомец должен быть удален, но получен статус {get_response.status_code}"
    
    @allure.story("Find Pets")
    @allure.title("Поиск питомцев по статусу")
    @allure.description("Проверка поиска питомцев по статусу с валидацией статус-кода и JSON-схемы")
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status(self, class_pets_client: PetsClient, status: str):
        """Тест поиска питомцев по статусу"""
        with allure.step(f"Отправка GET запроса для поиска питомцев со статусом '{status}'"):
            response = class_pets_client.find_pets_by_status(status)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        with allure.step("Валидация JSON-схемы ответа через Pydantic"):
            pets_list = response.json()
            assert isinstance(pets_list, list), "Ответ должен быть списком"
            
            for pet_data in pets_list:
                pet = Pet(**pet_data)
                assert pet.status == status, f"Все питомцы должны иметь статус '{status}'"
    
    @allure.story("Validation")
    @allure.title("Валидация обязательных полей при создании")
    @allure.description("Проверка, что при создании питомца обязательные поля сохраняются корректно")
    def test_pet_required_fields_validation(self, class_pets_client: PetsClient):
        """Тест валидации обязательных полей"""
        with allure.step("Создание питомца с обязательными полями"):
            pet = Pet(name="Test Pet", status="available")
            response = class_pets_client.create_pet(pet)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code in [200, 201], \
                f"Ожидался статус 200 или 201, получен {response.status_code}. Ответ: {response.text}"
        
        with allure.step("Валидация сохранения обязательных полей"):
            response_pet = Pet(**response.json())
            assert response_pet.name == "Test Pet", "Имя питомца должно быть сохранено"
            assert response_pet.status == "available", "Статус питомца должен быть сохранен"
            assert response_pet.photo_urls is not None, "Список фото должен быть сохранен"
            
            # Очистка
            pet_id = response_pet.id
            if pet_id:
                class_pets_client.delete_pet(pet_id)

