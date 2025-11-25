import httpx
from typing import List, Optional
from petstore_api_tests.client.api_client import APIClient
from petstore_api_tests.models.pet import Pet, UpdatePet


class PetsClient(APIClient):
    """Клиент для работы с Pet API"""
    
    def create_pet(self, pet: Pet) -> httpx.Response:
        """Создает нового питомца"""
        pet_data = pet.model_dump(by_alias=True, exclude_none=True)
        return self.http_client.post("/pet", json=pet_data)
    
    def get_pet_by_id(self, pet_id: int) -> httpx.Response:
        """Получает питомца по ID"""
        return self.http_client.get(f"/pet/{pet_id}")
    
    def update_pet(self, pet: Pet) -> httpx.Response:
        """Обновляет существующего питомца"""
        pet_data = pet.model_dump(by_alias=True, exclude_none=True)
        return self.http_client.put("/pet", json=pet_data)
    
    def delete_pet(self, pet_id: int) -> httpx.Response:
        """Удаляет питомца по ID"""
        return self.http_client.delete(f"/pet/{pet_id}")
    
    def find_pets_by_status(self, status: str) -> httpx.Response:
        """Находит питомцев по статусу"""
        return self.http_client.get("/pet/findByStatus", params={"status": status})
    
    def update_pet_form_data(self, pet_id: int, name: Optional[str] = None, status: Optional[str] = None) -> httpx.Response:
        """Обновляет питомца через form-data"""
        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        return self.http_client.post(f"/pet/{pet_id}", data=data)

