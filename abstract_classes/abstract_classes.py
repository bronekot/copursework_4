from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AbstractAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        pass


class AbstractFileHandler(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        pass
