from typing import Optional, Dict, Any
import re


class Vacancy:
    """
    Класс для представления вакансии.

    Атрибуты:
        title (str): Заголовок вакансии.
        link (str): Ссылка на вакансию.
        salary (str): Зарплата.
        description (str): Описание вакансии.
    """

    def __init__(self, title: str, link: str, salary: Any, description: str):
        """
        Инициализация Vacancy.

        Аргументы:
            title (str): Заголовок вакансии.
            link (str): Ссылка на вакансию.
            salary (Any): Зарплата.
            description (str): Описание вакансии.
        """
        self.title = self._validate_string(title)
        self.link = self._validate_string(link)
        self.salary = self._validate_salary(salary)
        self.description = self._validate_string(description)

    def _validate_string(self, value: Any) -> str:
        """
        Проверить и преобразовать значение в строку.

        Аргументы:
            value (Any): Значение для проверки.

        Возвращает:
            str: Проверенное значение.
        """
        return str(value) if value is not None else ""

    def _validate_salary(self, salary: Any) -> str:
        """
        Проверить и форматировать зарплату.

        Аргументы:
            salary (Any): Зарплата для проверки.

        Возвращает:
            str: Отформатированная зарплата.
        """
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
        """
        Получить числовое значение зарплаты.

        Возвращает:
            int: Числовое значение зарплаты.
        """
        if self.salary == "Salary not specified":
            return 0

        numbers = re.findall(r"\d+", self.salary.replace(",", ""))

        if not numbers:
            return 0

        return max(map(int, numbers))

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Сравнить зарплату с другой вакансией (меньше).

        Аргументы:
            other (Vacancy): Другая вакансия.

        Возвращает:
            bool: True, если зарплата меньше.
        """
        return self._get_numeric_salary() < other._get_numeric_salary()

    def __le__(self, other: "Vacancy") -> bool:
        """
        Сравнить зарплату с другой вакансией (меньше или равно).

        Аргументы:
            other (Vacancy): Другая вакансия.

        Возвращает:
            bool: True, если зарплата меньше или равна.
        """
        return self._get_numeric_salary() <= other._get_numeric_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        """
        Сравнить зарплату с другой вакансией (больше).

        Аргументы:
            other (Vacancy): Другая вакансия.

        Возвращает:
            bool: True, если зарплата больше.
        """
        return self._get_numeric_salary() > other._get_numeric_salary()

    def __ge__(self, other: "Vacancy") -> bool:
        """
        Сравнить зарплату с другой вакансией (больше или равно).

        Аргументы:
            other (Vacancy): Другая вакансия.

        Возвращает:
            bool: True, если зарплата больше или равна.
        """
        return self._get_numeric_salary() >= other._get_numeric_salary()

    def __eq__(self, other: "Vacancy") -> bool:
        """
        Сравнить зарплату с другой вакансией (равно).

        Аргументы:
            other (Vacancy): Другая вакансия.

        Возвращает:
            bool: True, если зарплата равна.
        """
        return self._get_numeric_salary() == other._get_numeric_salary()

    def __ne__(self, other: "Vacancy") -> bool:
        """
        Сравнить зарплату с другой вакансией (не равно).

        Аргументы:
            other (Vacancy): Другая вакансия.

        Возвращает:
            bool: True, если зарплата не равна.
        """
        return self._get_numeric_salary() != other._get_numeric_salary()

    def __str__(self) -> str:
        """
        Получить строковое представление вакансии.

        Возвращает:
            str: Строковое представление вакансии.
        """
        return f"{self.title} ({self.salary})"

    def to_dict(self) -> Dict[str, str]:
        """
        Преобразовать вакансию в словарь.

        Возвращает:
            Dict[str, str]: Словарь с данными вакансии.
        """
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """
        Создать объект Vacancy из словаря.

        Аргументы:
            data (Dict[str, Any]): Словарь с данными вакансии.

        Возвращает:
            Vacancy: Объект вакансии.
        """
        return cls(
            title=data["title"],
            link=data["link"],
            salary=data["salary"],
            description=data["description"],
        )
