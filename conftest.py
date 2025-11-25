import pytest
import allure
from petstore_api_tests.client.pets_client import PetsClient
from petstore_api_tests.models.pet import Pet
from petstore_api_tests.utils.faker_utils import random_number


@pytest.fixture(scope="class")
def class_pets_client():
    """Фикстура для инициализации PetsClient на уровне класса"""
    client = PetsClient()
    yield client
    client.close()


@pytest.fixture(scope="function")
def function_pet(class_pets_client):
    """Фикстура для создания питомца перед тестом и удаления после теста"""
    # Создаем питомца
    pet = Pet(id=random_number(100000, 999999))
    create_response = class_pets_client.create_pet(pet)
    
    assert create_response.status_code in [200, 201], f"Не удалось создать питомца: {create_response.text}"
    pet_id = create_response.json().get("id") or pet.id
    
    yield pet_id
    
    # Удаляем питомца после теста
    delete_response = class_pets_client.delete_pet(pet_id)
    # Игнорируем ошибки при удалении (питомец может быть уже удален)


@pytest.fixture
def pet_data():
    """Фикстура для генерации тестовых данных питомца"""
    return Pet()

