import json
from typing import List, Dict, Any
from src.vacancies.vacancy import Vacancy


class JSONFileHandler:
    def __init__(self, filename: str = "data/vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy: list[Vacancy]):
        try:
            with open(self.filename, "a") as file:
                for v in vacancy:
                    file.write(json.dumps(v.to_dict()) + "\n")
                file.write("\n")
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")

    def get_vacancies(self) -> list[Vacancy]:
        try:
            with open(self.filename, "r") as file:
                data = [json.loads(line) for line in file]
                vacancies = [Vacancy.from_dict(vacancy) for vacancy in data]
                return vacancies
        except IOError as e:
            print(f"Ошибка чтения из файла: {e}")
            return []
