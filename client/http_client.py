import httpx
import allure
import json
from typing import Optional, Dict, Any
from petstore_api_tests.settings import settings


class HTTPClient(httpx.Client):
    """HTTP клиент с интеграцией Allure для логирования запросов и ответов"""
    
    def __init__(self, base_url: Optional[str] = None, **kwargs):
        base_url = base_url or settings.base_url
        super().__init__(base_url=base_url, timeout=30.0, **kwargs)
    
    @allure.step("GET запрос: {url}")
    def get(self, url: str, **kwargs) -> httpx.Response:
        """Выполняет GET запрос с логированием в Allure"""
        with allure.step(f"Параметры запроса: {kwargs}"):
            response = super().get(url, **kwargs)
        with allure.step(f"Статус ответа: {response.status_code}"):
            try:
                response_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
            except (ValueError, json.JSONDecodeError):
                response_body = response.text
            allure.attach(
                response_body,
                name="Response body",
                attachment_type=allure.attachment_type.JSON
            )
        return response
    
    @allure.step("POST запрос: {url}")
    def post(self, url: str, **kwargs) -> httpx.Response:
        """Выполняет POST запрос с логированием в Allure"""
        if "json" in kwargs:
            try:
                request_body = json.dumps(kwargs["json"], indent=2, ensure_ascii=False)
            except (TypeError, ValueError):
                request_body = str(kwargs["json"])
            allure.attach(
                request_body,
                name="Request body",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step(f"Параметры запроса: {kwargs}"):
            response = super().post(url, **kwargs)
        with allure.step(f"Статус ответа: {response.status_code}"):
            try:
                response_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
            except (ValueError, json.JSONDecodeError):
                response_body = response.text
            allure.attach(
                response_body,
                name="Response body",
                attachment_type=allure.attachment_type.JSON
            )
        return response
    
    @allure.step("PUT запрос: {url}")
    def put(self, url: str, **kwargs) -> httpx.Response:
        """Выполняет PUT запрос с логированием в Allure"""
        if "json" in kwargs:
            try:
                request_body = json.dumps(kwargs["json"], indent=2, ensure_ascii=False)
            except (TypeError, ValueError):
                request_body = str(kwargs["json"])
            allure.attach(
                request_body,
                name="Request body",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step(f"Параметры запроса: {kwargs}"):
            response = super().put(url, **kwargs)
        with allure.step(f"Статус ответа: {response.status_code}"):
            try:
                response_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
            except (ValueError, json.JSONDecodeError):
                response_body = response.text
            allure.attach(
                response_body,
                name="Response body",
                attachment_type=allure.attachment_type.JSON
            )
        return response
    
    @allure.step("DELETE запрос: {url}")
    def delete(self, url: str, **kwargs) -> httpx.Response:
        """Выполняет DELETE запрос с логированием в Allure"""
        with allure.step(f"Параметры запроса: {kwargs}"):
            response = super().delete(url, **kwargs)
        with allure.step(f"Статус ответа: {response.status_code}"):
            try:
                response_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
            except (ValueError, json.JSONDecodeError):
                response_body = response.text
            allure.attach(
                response_body,
                name="Response body",
                attachment_type=allure.attachment_type.JSON
            )
        return response

