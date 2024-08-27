from typing import Dict, Optional, Union


class Vacancy:
    def __init__(
        self,
        name: str,
        url: str,
        salary: Optional[Dict[str, Union[str, int]]],
        description: str,
    ):
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description

    def _get_numeric_salary(self) -> Optional[int]:
        """Возвращает числовую зарплату или None."""
        if self.salary:
            # Check if salary 'from' is a string and if it can be converted to int
            salary_from = self.salary.get("from")
            if isinstance(salary_from, str) and salary_from.isdigit():
                return int(salary_from)
            elif isinstance(salary_from, int):
                return salary_from
        return None

    def to_dict(self) -> Dict[str, Union[str, Dict[str, Union[str, int]]]]:
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }

    @staticmethod
    def from_dict(data: Dict[str, Union[str, Dict[str, Union[str, int]]]]) -> "Vacancy":
        return Vacancy(
            name=data.get("name", "Неизвестно"),
            url=data.get("url", ""),
            salary=data.get("salary"),
            description=data.get("description", "Нет описания"),
        )

    def __repr__(self) -> str:
        return f"Vacancy(name={self.name}, url={self.url}, salary={self.salary}, description={self.description})"
