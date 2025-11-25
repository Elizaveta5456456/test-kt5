import random
import string
from typing import List


def random_string(length: int = 10) -> str:
    """Генерирует случайную строку заданной длины"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def random_number(min_value: int = 1, max_value: int = 1000000) -> int:
    """Генерирует случайное число в заданном диапазоне"""
    return random.randint(min_value, max_value)


def random_list_of_strings(count: int = 3, length: int = 10) -> List[str]:
    """Генерирует список случайных строк"""
    return [random_string(length) for _ in range(count)]


def random_status() -> str:
    """Генерирует случайный статус для питомца"""
    return random.choice(["available", "pending", "sold"])

