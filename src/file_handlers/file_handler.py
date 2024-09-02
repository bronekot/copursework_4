import json
from typing import List, Dict, Any
from src.abstract_classes.abstract_classes import AbstractFileHandler
from src.vacancies.vacancy import Vacancy


class JSONFileHandler(AbstractFileHandler):
    def __init__(self, filename: str = "data/vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy: List[Vacancy]) -> None:
        try:
            with open(self.filename, "a") as file:
                if isinstance(vacancy, list):
                    for v in vacancy:
                        json.dump(v.to_dict(), file)
                        file.write("\n")
                else:
                    json.dump(vacancy.to_dict(), file)
                    file.write("\n")
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")

    def get_vacancies(self) -> List[Vacancy]:
        try:
            with open(self.filename, "r") as file:
                return [
                    Vacancy.from_dict(json.loads(line)) for line in file if line.strip()
                ]
        except IOError as e:
            print(f"Ошибка чтения из файла: {e}")
            return []

    def delete_vacancy(self, name: str, url: str) -> None:
        try:
            vacancies = self.get_vacancies()
            vacancies = [v for v in vacancies if not (v.name == name and v.url == url)]
            with open(self.filename, "w") as file:
                for v in vacancies:
                    json.dump(v.to_dict(), file)
                    file.write("\n")
        except IOError as e:
            print(f"Ошибка при удалении вакансии: {e}")
