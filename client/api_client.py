from petstore_api_tests.client.http_client import HTTPClient
from petstore_api_tests.settings import settings


class APIClient:
    """Базовый клиент для работы с API"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.base_url
        self._http_client = None
    
    @property
    def http_client(self) -> HTTPClient:
        """Возвращает HTTP клиент с базовыми настройками"""
        if self._http_client is None:
            self._http_client = HTTPClient(base_url=self.base_url)
        return self._http_client
    
    def close(self):
        """Закрывает HTTP клиент"""
        if self._http_client:
            self._http_client.close()
            self._http_client = None

