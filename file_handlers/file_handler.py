import json
from abstract_classes.abstract_classes import AbstractFileHandler
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)


class JSONFileHandler(AbstractFileHandler):
    def __init__(self, filename: str = "vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        vacancies = self.get_vacancies()
        if not any(v["link"] == vacancy["link"] for v in vacancies):
            vacancies.append(vacancy)
            self._save_vacancies(vacancies)
            logging.info(f"Added vacancy: {vacancy['title']}")

    def get_vacancies(self) -> List[Dict[str, Any]]:
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logging.warning(f"File {self.filename} not found. Returning empty list.")
            return []
        except json.JSONDecodeError:
            logging.error(
                f"Error decoding JSON from {self.filename}. Returning empty list."
            )
            return []

    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v["link"] != vacancy["link"]]
        self._save_vacancies(vacancies)
        logging.info(f"Deleted vacancy: {vacancy['title']}")

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        try:
            with open(self.filename, "w") as file:
                json.dump(vacancies, file, indent=2)
        except IOError as e:
            logging.error(f"Error saving vacancies to {self.filename}: {e}")
