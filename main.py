import logging
from src.api.hh_api import HeadHunterAPI
from src.vacancies.vacancy import Vacancy
from src.file_handlers.file_handler import JSONFileHandler
from typing import List

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def filter_vacancies(vacancies, filter_words):
    """
    Фильтровать вакансии по ключевым словам.

    Аргументы:
        vacancies (List[Vacancy]): Список вакансий.
        filter_words (List[str]): Ключевые слова для фильтрации.

    Возвращает:
        List[Vacancy]: Отфильтрованный список вакансий.
    """
    return [
        v
        for v in vacancies
        if all(word.lower() in v.description.lower() for word in filter_words)
    ]


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    if not salary_range.strip():
        return vacancies

    try:
        parts = salary_range.split("-")
        if len(parts) == 2:
            min_salary, max_salary = map(int, parts)
        elif len(parts) == 1:
            min_salary = max_salary = int(parts[0])
        else:
            raise ValueError
    except ValueError:
        print("Некорректный формат диапазона зарплат.")
        return []

    def salary_in_range(salary):
        if not salary:
            return False
        salary_from = salary.get("from")
        salary_to = salary.get("to")

        if salary_from is None and salary_to is None:
            return False
        if salary_from is None:
            return salary_to >= min_salary
        if salary_to is None:
            return salary_from <= max_salary

        return salary_from <= max_salary and salary_to >= min_salary

    return [v for v in vacancies if salary_in_range(v.salary)]


def sort_vacancies(vacancies):
    """
    Сортировать вакансии по убыванию зарплаты.

    Аргументы:
        vacancies (List[Vacancy]): Список вакансий.

    Возвращает:
        List[Vacancy]: Отсортированный список вакансий.
    """
    return sorted(vacancies, key=lambda v: v._get_numeric_salary() or 0, reverse=True)


def get_top_vacancies(vacancies, top_n):
    """
    Получить топ N вакансий.

    Аргументы:
        vacancies (List[Vacancy]): Список вакансий.
        top_n (int): Количество вакансий для отображения.

    Возвращает:
        List[Vacancy]: Топ N вакансий.
    """
    return vacancies[:top_n]


def print_vacancies(vacancies):
    """
    Печать вакансий.

    Аргументы:
        vacancies (List[Vacancy]): Список вакансий.
    """
    if not vacancies:
        print("Нет вакансий для отображения.")
    for vacancy in vacancies:
        print(vacancy)


def user_interaction():
    # Initialize the API instance
    api = HeadHunterAPI()
    json_handler = JSONFileHandler()

    # platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (например, '100000 - 150000'): ")

    # Fetch vacancies using the API
    vacancies_data = api.get_vacancies(query=search_query, per_page=100, page=0)
    vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

    print(f"INFO: Получено {len(vacancies)} вакансий для запроса '{search_query}'.")

    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    json_handler.add_vacancy(top_vacancies)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
