from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AbstractAPI(ABC):
    """
    Абстрактный класс для API.

    Методы:
        get_vacancies(keyword: str) -> List[Dict[str, Any]]:
            Получить список вакансий по ключевому слову.
    """

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получить список вакансий по ключевому слову.

        Аргументы:
            keyword (str): Ключевое слово для поиска вакансий.

        Возвращает:
            List[Dict[str, Any]]: Список вакансий.
        """
        pass


class AbstractFileHandler(ABC):
    """
    Абстрактный класс для работы с файлами.

    Методы:
        add_vacancy(vacancy: Dict[str, Any]) -> None:
            Добавить вакансию в файл.
        get_vacancies() -> List[Dict[str, Any]]:
            Получить список вакансий из файла.
        delete_vacancy(vacancy: Dict[str, Any]) -> None:
            Удалить вакансию из файла.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
        Добавить вакансию в файл.

        Аргументы:
            vacancy (Dict[str, Any]): Вакансия для добавления.
        """
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получить список вакансий из файла.

        Возвращает:
            List[Dict[str, Any]]: Список вакансий.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, name: str, url: str) -> None:
        """
        Удалить вакансию из файла.

        Аргументы:
            name (str): Имя вакансии.
            url (str): URL вакансии.
        """
        pass
