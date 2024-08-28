# Файл: tests/test_vacancy_system.py

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vacancies.vacancy import Vacancy
from src.api.hh_api import HeadHunterAPI
from src.file_handlers.file_handler import JSONFileHandler
from main import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
)


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Вакансия 1", "url1", {"from": 100000, "to": 150000}, "Описание 1"),
        Vacancy("Вакансия 2", "url2", {"from": 80000, "to": 120000}, "Описание 2"),
        Vacancy("Вакансия 3", "url3", None, "Описание 3"),
        Vacancy("Вакансия 4", "url4", {"from": 150000, "to": 200000}, "Описание 4"),
    ]


def test_filter_vacancies(sample_vacancies):
    filtered = filter_vacancies(sample_vacancies, ["Описание"])
    assert len(filtered) == 4

    filtered = filter_vacancies(sample_vacancies, ["1"])
    assert len(filtered) == 1
    assert filtered[0].name == "Вакансия 1"


def test_get_vacancies_by_salary(sample_vacancies):
    # Тест 1: Диапазон включает нижнюю границу первой вакансии
    filtered = get_vacancies_by_salary(sample_vacancies, "90000-130000")
    assert len(filtered) == 2
    assert set(v.name for v in filtered) == {"Вакансия 1", "Вакансия 2"}

    # Тест 2: Диапазон включает первую и вторую вакансии полностью, и нижнюю границу четвертой
    filtered = get_vacancies_by_salary(sample_vacancies, "100000-150000")
    assert len(filtered) == 3
    assert set(v.name for v in filtered) == {"Вакансия 1", "Вакансия 2", "Вакансия 4"}

    # Тест 3: Диапазон включает нижнюю границу четвертой вакансии и верхнюю границу первой и второй
    filtered = get_vacancies_by_salary(sample_vacancies, "150000-200000")
    assert len(filtered) == 2
    assert set(v.name for v in filtered) == {"Вакансия 1", "Вакансия 4"}

    # Тест 4: Диапазон пересекается с тремя вакансиями
    filtered = get_vacancies_by_salary(sample_vacancies, "140000-160000")
    assert len(filtered) == 2
    assert set(v.name for v in filtered) == {"Вакансия 1", "Вакансия 4"}

    # Тест 5: Диапазон не включает ни одной вакансии
    filtered = get_vacancies_by_salary(sample_vacancies, "200000-300000")
    assert len(filtered) == 1

    # Тест 6: Проверка вакансии с открытым верхним пределом
    sample_vacancies.append(
        Vacancy("Вакансия 5", "url5", {"from": 180000}, "Описание 5")
    )
    filtered = get_vacancies_by_salary(sample_vacancies, "170000-190000")
    assert len(filtered) == 2
    assert set(v.name for v in filtered) == {"Вакансия 4", "Вакансия 5"}

    # Тест 7: Проверка граничного случая
    filtered = get_vacancies_by_salary(sample_vacancies, "150000-150000")
    assert len(filtered) == 2
    assert set(v.name for v in filtered) == {"Вакансия 1", "Вакансия 4"}

    # Дополнительные тесты
    sample_vacancies.append(Vacancy("Вакансия 6", "url6", {"to": 120000}, "Описание 6"))
    filtered = get_vacancies_by_salary(sample_vacancies, "110000-130000")
    assert len(filtered) == 3
    assert set(v.name for v in filtered) == {"Вакансия 1", "Вакансия 2", "Вакансия 6"}

    sample_vacancies.append(Vacancy("Вакансия 7", "url7", None, "Описание 7"))
    filtered = get_vacancies_by_salary(sample_vacancies, "100000-200000")
    assert len(filtered) == 5
    assert set(v.name for v in filtered) == {
        "Вакансия 1",
        "Вакансия 2",
        "Вакансия 4",
        "Вакансия 5",
        "Вакансия 6",
    }

    # Тест на пустой ввод
    filtered = get_vacancies_by_salary(sample_vacancies, "")
    assert len(filtered) == 0

    # Тест на некорректный формат ввода
    filtered = get_vacancies_by_salary(sample_vacancies, "invalid-input")
    assert len(filtered) == 0


def test_sort_vacancies(sample_vacancies):
    sorted_vacancies = sort_vacancies(sample_vacancies)
    assert sorted_vacancies[0].name == "Вакансия 4"
    assert sorted_vacancies[-1].name == "Вакансия 3"


def test_get_top_vacancies(sample_vacancies):
    top = get_top_vacancies(sample_vacancies, 2)
    assert len(top) == 2
    assert top[0].name == "Вакансия 1"
    assert top[1].name == "Вакансия 2"


def test_headhunter_api():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": [{"name": "Тестовая вакансия"}]}
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python", 1, 0)

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Тестовая вакансия"


def test_json_file_handler():
    with patch("builtins.open") as mock_open:
        handler = JSONFileHandler()
        vacancy = Vacancy(
            "Тестовая вакансия", "test_url", {"from": 100000}, "Тестовое описание"
        )

        handler.add_vacancy([vacancy])

        mock_open.assert_called_once_with("data/vacancies.json", "a")
        mock_open.return_value.__enter__().write.assert_called()


def test_vacancy_to_dict():
    vacancy = Vacancy(
        "Тестовая вакансия", "test_url", {"from": 100000}, "Тестовое описание"
    )
    vacancy_dict = vacancy.to_dict()

    assert vacancy_dict["name"] == "Тестовая вакансия"
    assert vacancy_dict["url"] == "test_url"
    assert vacancy_dict["salary"] == {"from": 100000}
    assert vacancy_dict["description"] == "Тестовое описание"


def test_vacancy_from_dict():
    vacancy_dict = {
        "name": "Тестовая вакансия",
        "url": "test_url",
        "salary": {"from": 100000},
        "description": "Тестовое описание",
    }
    vacancy = Vacancy.from_dict(vacancy_dict)

    assert vacancy.name == "Тестовая вакансия"
    assert vacancy.url == "test_url"
    assert vacancy.salary == {"from": 100000}
    assert vacancy.description == "Тестовое описание"


def test_get_numeric_salary():
    vacancy_with_salary = Vacancy("Тест", "url", {"from": 100000}, "Описание")
    assert vacancy_with_salary._get_numeric_salary() == 100000

    vacancy_without_salary = Vacancy("Тест", "url", None, "Описание")
    assert vacancy_without_salary._get_numeric_salary() is None

    vacancy_with_string_salary = Vacancy("Тест", "url", {"from": "100000"}, "Описание")
    assert vacancy_with_string_salary._get_numeric_salary() == 100000
