from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional, Union
from petstore_api_tests.utils.faker_utils import random_string, random_number, random_list_of_strings, random_status


class Category(BaseModel):
    """Модель категории питомца"""
    id: int = Field(default_factory=lambda: random_number(), description="ID категории")
    name: str = Field(default_factory=lambda: random_string(), description="Название категории")


class Tag(BaseModel):
    """Модель тега питомца"""
    id: int = Field(default_factory=lambda: random_number(), description="ID тега")
    name: str = Field(default_factory=lambda: random_string(), description="Название тега")


class Pet(BaseModel):
    """Модель питомца для PetStore API"""
    id: Optional[int] = Field(default=None, description="Уникальный идентификатор питомца")
    category: Optional[Category] = Field(default=None, description="Категория питомца")
    name: str = Field(default_factory=lambda: random_string(), description="Имя питомца")
    photo_urls: List[Optional[str]] = Field(
        default_factory=lambda: random_list_of_strings(2, 20),
        alias="photoUrls",
        description="Список URL фотографий"
    )
    
    @field_validator('photo_urls', mode='before')
    @classmethod
    def filter_none_photo_urls(cls, v):
        """Фильтрует None значения из списка photoUrls"""
        if isinstance(v, list):
            return [url for url in v if url is not None]
        return v
    
    tags: Optional[List[Tag]] = Field(default=None, description="Список тегов")
    status: str = Field(
        default_factory=random_status,
        description="Статус питомца: available, pending, sold"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": 0,
                "category": {
                    "id": 0,
                    "name": "string"
                },
                "name": "doggie",
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }
        }
    )


class UpdatePet(BaseModel):
    """Модель для обновления питомца (необязательные поля)"""
    id: Optional[int] = Field(default=None, description="ID питомца")
    name: Optional[str] = Field(default_factory=lambda: random_string(), description="Имя питомца")
    status: Optional[str] = Field(default_factory=random_status, description="Статус питомца")

