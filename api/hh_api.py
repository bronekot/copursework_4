import requests
from requests.exceptions import RequestException
from abstract_classes.abstract_classes import AbstractAPI
from config import BASE_URL
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)


class HeadHunterAPI(AbstractAPI):
    """
    Класс для взаимодействия с API HeadHunter.

    Атрибуты:
        base_url (str): Базовый URL для запросов.
        headers (Dict[str, str]): Заголовки для запросов.
    """

    def __init__(self):
        """
        Инициализация HeadHunterAPI.
        """
        self.base_url = BASE_URL
        self.headers = {"User-Agent": "HH-User-Agent"}

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получить список вакансий по ключевому слову.

        Аргументы:
            keyword (str): Ключевое слово для поиска вакансий.

        Возвращает:
            List[Dict[str, Any]]: Список вакансий.
        """
        params = {"text": keyword, "per_page": 100, "page": 0}
        all_vacancies = []

        while len(all_vacancies) < 500:  # Ограничиваем количество вакансий до 500
            try:
                response = requests.get(
                    f"{self.base_url}/vacancies", headers=self.headers, params=params
                )
                response.raise_for_status()
                data = response.json()
                vacancies = data["items"]
                if not vacancies:
                    break
                all_vacancies.extend(vacancies)
                params["page"] += 1
                logging.info(
                    f"Получено {len(vacancies)} вакансий. Всего: {len(all_vacancies)}"
                )
            except RequestException as e:
                logging.error(f"Error fetching vacancies: {e}")
                break

        return all_vacancies
