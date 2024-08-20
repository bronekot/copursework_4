import logging
from api.hh_api import HeadHunterAPI
from vacancies.vacancy import Vacancy
from file_handlers.file_handler import JSONFileHandler

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    hh_api = HeadHunterAPI()
    file_handler = JSONFileHandler()

    while True:
        print("\n1. Поиск вакансий")
        print("2. Показать топ N вакансий")
        print("3. Отфильтровать вакансии по ключевому слову")
        print("4. Отфильтровать вакансии по диапазону зарплаты")
        print("5. Показать статистику")
        print("6. Выход")
        choice = input("Выбери пункт меню: ")

        if choice == "1":
            keyword = input("Введите ключевое слово для поиска: ")
            try:
                vacancies_data = hh_api.get_vacancies(keyword)
                vacancies = []
                for v in vacancies_data:
                    try:
                        vacancy = Vacancy(
                            v["name"],
                            v["alternate_url"],
                            v["salary"],
                            v["snippet"]["requirement"],
                        )
                        vacancies.append(vacancy)
                        file_handler.add_vacancy(vacancy.to_dict())
                    except Exception as e:
                        logging.error(f"Ошибка при обработке вакансии: {e}")
                print(f"Найдено и сохранено {len(vacancies)} вакансий")
            except Exception as e:
                logging.error(f"Произошла ошибка: {e}")

        elif choice == "2":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print(
                    "Вакансии не найдены. Пожалуйста, выполните поиск вакансий сначала."
                )
                continue
            try:
                n = int(input("Введите количество топ вакансий для показа: "))
                logging.debug(f"Загрузка {len(vacancies)} вакансий из файла")
                vacancies = [Vacancy.from_dict(v) for v in vacancies]
                logging.debug(f"Загружено {len(vacancies)} объектов Vacancy")
                logging.debug(f"Пример вакансии: {vacancies[0]}")
                logging.debug(f"Пример зарплаты вакансии: {vacancies[0].salary}")
                logging.debug(
                    f"Числовая зарплата вакансии: {vacancies[0]._get_numeric_salary()}"
                )
                top_vacancies = sorted(vacancies, reverse=True)[:n]
                logging.debug(f"Сортировка вакансий, показ топ {n}")
                for vacancy in top_vacancies:
                    print(vacancy)
            except ValueError as e:
                logging.error(f"Некорректный ввод: {e}")
                print("Пожалуйста, введите корректное число.")
            except Exception as e:
                logging.error(f"Произошла ошибка: {e}", exc_info=True)

        elif choice == "3":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print(
                    "Вакансии не найдены. Пожалуйста, выполните поиск вакансий сначала."
                )
                continue
            keyword = input("Введите ключевое слово для фильтрации вакансий: ")
            vacancies = [Vacancy.from_dict(v) for v in vacancies]
            filtered_vacancies = [
                v for v in vacancies if keyword.lower() in v.description.lower()
            ]
            if filtered_vacancies:
                for vacancy in filtered_vacancies:
                    print(vacancy)
            else:
                print("Вакансии, соответствующие ключевому слову, не найдены.")

        elif choice == "4":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print(
                    "Вакансии не найдены. Пожалуйста, выполните поиск вакансий сначала."
                )
                continue
            try:
                min_salary = int(input("Введите минимальную зарплату: "))
                max_salary = int(input("Введите максимальную зарплату: "))
                vacancies = [Vacancy.from_dict(v) for v in vacancies]
                filtered_vacancies = [
                    v
                    for v in vacancies
                    if min_salary <= v._get_numeric_salary() <= max_salary
                ]
                if filtered_vacancies:
                    for vacancy in filtered_vacancies:
                        print(vacancy)
                else:
                    print("Вакансии в указанном диапазоне зарплаты не найдены.")
            except ValueError:
                print("Пожалуйста, введите корректные числа для диапазона зарплаты.")

        elif choice == "5":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print(
                    "Вакансии не найдены. Пожалуйста, выполните поиск вакансий сначала."
                )
                continue
            show_statistics(vacancies)

        elif choice == "6":
            print("Спасибо за использование программы. До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


def show_statistics(vacancies):
    """
    Показать статистику по вакансиям.

    Аргументы:
        vacancies (List[Dict[str, Any]]): Список вакансий для анализа.
    """
    total_vacancies = len(vacancies)
    salaries = [v["salary"] for v in vacancies if v["salary"] != "Salary not specified"]
    avg_salary = (
        sum(Vacancy.from_dict(v)._get_numeric_salary() for v in vacancies)
        / total_vacancies
        if total_vacancies
        else 0
    )

    print(f"Всего вакансий: {total_vacancies}")
    print(f"Средняя зарплата: {avg_salary:.2f}")


if __name__ == "__main__":
    user_interaction()
