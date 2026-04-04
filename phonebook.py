import math
from unittest import case
import json

file_name = "contacts.json"



#contacts = []
# contacts = [
#     {"id": 1, "name": "Иван", "phone": "12345", "comment": "друг"},
#     {"id": 2, "name": "Анна", "phone": "67890", "comment": "работа"},
#     {"id": 3, "name": "Петр", "phone": "55555", "comment": "сосед"},
#     {"id": 4, "name": "Мария", "phone": "11111", "comment": "семья"},
#     {"id": 4, "name": "Анна", "phone": "66600", "comment": "семья"},
# ]

def load_contacts(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            print("Ошибка: файл содержит некорректные данные")
            return []

    except FileNotFoundError:
        print("Файл с контактами не найден. Будет создан новый.")
        return []

    except json.JSONDecodeError:
        print("Ошибка чтения JSON. Будет использован пустой список контактов.")
        return []

def save_contacts(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Контакты сохранены в файл")

    except OSError:
        print("Ошибка при сохранении файла")


contacts = load_contacts(file_name)

def show_menu():
    print("\nТелефонный справочник")
    print("1. Показать все контакты")
    print("2. Добавить контакт")
    print("3. Удалить контакт")
    print("4. Найти контакт")
    print("5. Редактировать контакт")
    print("6. Сохранить контакты")
    print("0. Выход")


def show_contacts(data):
    if not data:
        print("Список контактов пуст")
        return

    # for contact in data: # осталось от тестов
    #     print(contact)
    for contact in data: # делаем красивый вывод
        print(
            f'ID: {contact["id"]}, '
            f'Имя: {contact["name"]}, '
            f'Телефон: {contact["phone"]}, '
            f'Комментарий: {contact["comment"]}'
        )

def get_next_id(data):
    if not data:
        return 1

    max_id = 0
    for contact in data:
        if contact["id"] > max_id:
            max_id = contact["id"]

    return max_id + 1

def add_contact(data):
    name = input("Введите имя: ").strip()
    if not name:
        print("Имя не может быть пустым")
        return

    phone = input("Введите телефон: ").strip()
    if not phone:
        print("Телефон не может быть пустым")
        return

    # проверка: только цифры
    if not phone.isdigit():
        print("Телефон должен содержать только цифры")
        return

    comment = input("Введите комментарий: ").strip()

    contact = {
        "id": get_next_id(data),
        "name": name,
        "phone": phone,
        "comment": comment
    }

    data.append(contact)

    print(
        f'Контакт добавлен: '
        f'ID: {contact["id"]}, '
        f'Имя: {contact["name"]}, '
        f'Телефон: {contact["phone"]}'
    )

def delete_contact(data):
    contact_id = input("Введите ID контакта для удаления: ").strip()

    if not contact_id.isdigit(): #.isdigit() защита от отрицательного значения и всего того, что не цифра
        print("ID должен быть числом")
        return

    contact_id = int(contact_id)

    for contact in data:
        if contact["id"] == contact_id:
            print( # сделал сначала вывод, чтобы показать какой контакт удалён
                f'Удалён контакт: '
                f'ID: {contact["id"]}, '
                f'Имя: {contact["name"]}, '
                f'Телефон: {contact["phone"]}, '
                f'Комментарий: {contact["comment"]}'
            )
            data.remove(contact)
            #print("Контакт удалён")
            return

    print("Контакт с таким ID не найден")

def find_contacts(data):

    print("\nВыберите условия поиска в Меню")
    print("1. По имени")
    print("2. По номеру телефона")
    print("3. По комментарию")
    print("4. По ID")
    choice = input("Выберите пункт меню: ").strip()

    query = None # добавил, чтобы пайчарм не светил жёлтым переменную
    found = []

    match choice:
        case "1":
            query = input("Введите ИМЯ для поиска: ").strip().lower()
            for contact in data:
                if query in contact["name"].lower():
                    found.append(contact)
        case "2":
            query = input("Введите НОМЕР ТЕЛЕФОНА для поиска: ").strip().lower()
            for contact in data:
                if query in contact["phone"]:
                    found.append(contact)
        case "3":
            query = input("Введите КОММЕНТАРИЙ для поиска: ").strip().lower()
            for contact in data:
                if query in contact["comment"].lower():
                    found.append(contact)
        case "4":
            query = input("Введите ID для поиска: ").strip().lower()
            for contact in data:
                if query == str(contact["id"]):
                    found.append(contact)
        case _:
            print("Неверный пункт меню")
            return

    if not query:
        print("Пустой запрос")
        return

    if not found:
        print("Ничего не найдено")
        return

    print("\nНайденные контакты:")
    for contact in found:
        print(
            f'ID: {contact["id"]}, '
            f'Имя: {contact["name"]}, '
            f'Телефон: {contact["phone"]}, '
            f'Комментарий: {contact["comment"]}'
        )


def edit_contact(data):
    contact_id = input("Введите ID контакта для редактирования: ").strip()

    if not contact_id.isdigit():
        print("ID должен быть числом")
        return

    contact_id = int(contact_id)

    for contact in data:
        if contact["id"] == contact_id:
            print("\nТекущие данные контакта:")
            print(
                f'ID: {contact["id"]}, '
                f'Имя: {contact["name"]}, '
                f'Телефон: {contact["phone"]}, '
                f'Комментарий: {contact["comment"]}'
            )

            new_name = input("Введите новое имя (Enter - оставить старое): ").strip()
            new_phone = input("Введите новый телефон (Enter - оставить старый): ").strip()
            new_comment = input("Введите новый комментарий (Enter - оставить старый): ").strip()

            if new_name:
                contact["name"] = new_name

            if new_phone:
                if not new_phone.isdigit():
                    print("Телефон должен содержать только цифры")
                    return
                contact["phone"] = new_phone

            if new_comment:
                contact["comment"] = new_comment

            print("\nКонтакт обновлён:")
            print(
                f'ID: {contact["id"]}, '
                f'Имя: {contact["name"]}, '
                f'Телефон: {contact["phone"]}, '
                f'Комментарий: {contact["comment"]}'
            )
            return

    print("Контакт с таким ID не найден")


def main():
    prg_on = True
    while prg_on:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        match choice:
            case "1":
                show_contacts(contacts)
            case "2":
                add_contact(contacts)
            case "3":
                delete_contact(contacts)
            case "4":
                find_contacts(contacts)
            case "5":
                edit_contact(contacts)
            case "6":
                save_contacts(file_name, contacts)
            case "0":
                save_choice = input("Сохранить изменения перед выходом? (y/n): ").strip().lower()

                if save_choice == "y":
                    save_contacts(file_name, contacts)

                print("Выход из программы")
                break
            case _:
                print("Неверный пункт меню")

if __name__ == "__main__":
    main()