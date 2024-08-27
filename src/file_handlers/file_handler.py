import json
from typing import List, Dict, Any


class JSONFileHandler:
    def __init__(self, filename: str = "data/vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy: Dict[str, Any]):
        try:
            with open(self.filename, "a") as file:
                json.dump(vacancy, file)
                file.write("\n")
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")

    def get_vacancies(self) -> List[Dict[str, Any]]:
        try:
            with open(self.filename, "r") as file:
                return [json.loads(line) for line in file]
        except IOError as e:
            print(f"Ошибка чтения из файла: {e}")
            return []
