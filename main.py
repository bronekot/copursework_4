import logging
from api.hh_api import HeadHunterAPI
from vacancies.vacancy import Vacancy
from file_handlers.file_handler import JSONFileHandler


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def user_interaction():
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
            keyword = input("Enter search keyword: ")
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
                        logging.error(f"Error processing vacancy: {e}")
                print(f"Found and saved {len(vacancies)} vacancies")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

        elif choice == "2":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print("No vacancies found. Please search for vacancies first.")
                continue
            try:
                n = int(input("Enter number of top vacancies to show: "))
                logging.debug(f"Loading {len(vacancies)} vacancies from file")
                vacancies = [Vacancy.from_dict(v) for v in vacancies]
                logging.debug(f"Loaded {len(vacancies)} Vacancy objects")
                logging.debug(f"Sample vacancy: {vacancies[0]}")
                logging.debug(f"Sample vacancy salary: {vacancies[0].salary}")
                logging.debug(
                    f"Sample vacancy numeric salary: {vacancies[0]._get_numeric_salary()}"
                )
                top_vacancies = sorted(vacancies, reverse=True)[:n]
                logging.debug(f"Sorted vacancies, showing top {n}")
                for vacancy in top_vacancies:
                    print(vacancy)
            except ValueError as e:
                logging.error(f"Invalid input: {e}")
                print("Please enter a valid number.")
            except Exception as e:
                logging.error(f"An error occurred: {e}", exc_info=True)

        elif choice == "3":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print("No vacancies found. Please search for vacancies first.")
                continue
            keyword = input("Enter keyword to filter vacancies: ")
            vacancies = [Vacancy.from_dict(v) for v in vacancies]
            filtered_vacancies = [
                v for v in vacancies if keyword.lower() in v.description.lower()
            ]
            if filtered_vacancies:
                for vacancy in filtered_vacancies:
                    print(vacancy)
            else:
                print("No vacancies found matching the keyword.")

        elif choice == "4":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print("No vacancies found. Please search for vacancies first.")
                continue
            try:
                min_salary = int(input("Enter minimum salary: "))
                max_salary = int(input("Enter maximum salary: "))
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
                    print("No vacancies found in the specified salary range.")
            except ValueError:
                print("Please enter valid numbers for salary range.")

        elif choice == "5":
            vacancies = file_handler.get_vacancies()
            if not vacancies:
                print("No vacancies found. Please search for vacancies first.")
                continue
            show_statistics(vacancies)

        elif choice == "6":
            print("Thank you for using the program. Goodbye!")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


def show_statistics(vacancies):
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
