from typing import Optional, Dict, Any
import re


class Vacancy:
    def __init__(self, title: str, link: str, salary: Any, description: str):
        self.title = self._validate_string(title)
        self.link = self._validate_string(link)
        self.salary = self._validate_salary(salary)
        self.description = self._validate_string(description)

    def _validate_string(self, value: Any) -> str:
        return str(value) if value is not None else ""

    def _validate_salary(self, salary: Any) -> str:
        if isinstance(salary, str):
            return salary
        if not salary:
            return "Salary not specified"
        from_salary = salary.get("from")
        to_salary = salary.get("to")
        currency = salary.get("currency", "")
        if from_salary and to_salary:
            return f"{from_salary}-{to_salary} {currency}"
        elif from_salary:
            return f"from {from_salary} {currency}"
        elif to_salary:
            return f"up to {to_salary} {currency}"
        return "Salary not specified"

    def _get_numeric_salary(self) -> int:
        if self.salary == "Salary not specified":
            return 0

        # Extract all numbers from the salary string
        numbers = re.findall(r"\d+", self.salary.replace(",", ""))

        if not numbers:
            return 0

        # If there's more than one number, take the larger one
        return max(map(int, numbers))

    def __lt__(self, other: "Vacancy") -> bool:
        return self._get_numeric_salary() < other._get_numeric_salary()

    def __le__(self, other: "Vacancy") -> bool:
        return self._get_numeric_salary() <= other._get_numeric_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        return self._get_numeric_salary() > other._get_numeric_salary()

    def __ge__(self, other: "Vacancy") -> bool:
        return self._get_numeric_salary() >= other._get_numeric_salary()

    def __eq__(self, other: "Vacancy") -> bool:
        return self._get_numeric_salary() == other._get_numeric_salary()

    def __ne__(self, other: "Vacancy") -> bool:
        return self._get_numeric_salary() != other._get_numeric_salary()

    def __str__(self) -> str:
        return f"{self.title} ({self.salary})"

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        return cls(
            title=data["title"],
            link=data["link"],
            salary=data["salary"],
            description=data["description"],
        )
