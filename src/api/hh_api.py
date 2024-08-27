import requests
from requests.exceptions import RequestException
from src.abstract_classes.abstract_classes import AbstractAPI
from config import BASE_URL
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)


class HeadHunterAPI(AbstractAPI):
    """
    Класс для взаимодействия с API HeadHunter.
    """

    def __init__(self):
        """
        Инициализация HeadHunterAPI.
        """
        self.base_url = BASE_URL
        self.headers = {"User-Agent": "HH-User-Agent"}

    def get_vacancies(
        self, query: str, per_page: int, page: int
    ) -> List[Dict[str, Any]]:
        """
        Получить список вакансий по запросу.

        Аргументы:
            query (str): Запрос для поиска вакансий.
            per_page (int): Количество вакансий на странице.
            page (int): Номер страницы для получения.

        Возвращает:
            List[Dict[str, Any]]: Список вакансий.
        """
        params = {"text": query, "per_page": per_page, "page": page}
        try:
            response = requests.get(
                f"{self.base_url}/vacancies", headers=self.headers, params=params
            )
            response.raise_for_status()
            data = response.json()
            vacancies = data.get("items", [])
            logging.info(f"Получено {len(vacancies)} вакансий для запроса '{query}'.")
            return vacancies
        except RequestException as e:
            logging.error(f"Error fetching vacancies: {e}")
            return []
