import json
import os

class Book:
    """Класс для представления книги"""
    def __init__(self, title, author, genre, year, description, is_read=False, is_favorite=False):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.description = description
        self.is_read = is_read
        self.is_favorite = is_favorite

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Library:
    """Класс для управления библиотекой"""
    def __init__(self, storage_file='library.json'):
        self.storage_file = storage_file
        self.books = self.load_from_file()

    def load_from_file(self):
        """Восстановление данных из файла"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Book.from_dict(item) for item in data]
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_to_file(self):
        """Сохранение данных в файл"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self):
        """Добавление новой книги"""
        print("\n--- Добавление новой книги ---")
        title = input("Название: ")
        author = input("Автор: ")
        genre = input("Жанр: ")
        while True:
            try:
                year = int(input("Год издания: "))
                break
            except ValueError:
                print("Ошибка: год должен быть числом.")
        description = input("Краткое описание: ")
        
        new_book = Book(title, author, genre, year, description)
        self.books.append(new_book)
        self.save_to_file()
        print("Книга успешно добавлена!")

    def delete_book(self):
        """Удаление книги"""
        self.show_books()
        try:
            idx = int(input("\nВведите номер (ID) книги для удаления: "))
            if 0 <= idx < len(self.books):
                removed = self.books.pop(idx)
                self.save_to_file()
                print(f"Книга '{removed.title}' удалена.")
            else:
                print("Ошибка: неверный номер.")
        except ValueError:
            print("Ошибка: введите число.")

    def search_books(self):
        """Поиск книг по ключевым словам"""
        query = input("\nВведите ключевое слово для поиска (в названии, авторе или описании): ").lower()
        results = [b for b in self.books if query in b.title.lower() or 
                   query in b.author.lower() or query in b.description.lower()]
        
        print(f"\nРезультаты поиска ({len(results)}):")
        self.show_books(results)

    def change_status(self):
        """Изменение статуса 'прочитано' и управление Избранным"""
        self.show_books()
        try:
            idx = int(input("\nВведите номер книги для изменения: "))
            if 0 <= idx < len(self.books):
                print("1. Изменить статус (прочитана/не прочитана)")
                print("2. Добавить/Удалить из Избранного")
                choice = input("Выберите действие: ")
                
                if choice == '1':
                    self.books[idx].is_read = not self.books[idx].is_read
                elif choice == '2':
                    self.books[idx].is_favorite = not self.books[idx].is_favorite
                
                self.save_to_file()
                print("Статус успешно обновлен!")
            else:
                print("Ошибка: неверный номер.")
        except ValueError:
            print("Ошибка: введите число.")

    def get_favorites_and_recs(self):
        """Просмотр избранного и рекомендаций"""
        favorites = [b for b in self.books if b.is_favorite]
        print("\n--- ВАШЕ ИЗБРАННОЕ ---")
        self.show_books(favorites)

        # Рекомендации: книги того же жанра, что и избранные, но еще не прочитанные
        fav_genres = {b.genre for b in favorites}
        recommendations = [b for b in self.books if b.genre in fav_genres and not b.is_read and not b.is_favorite]
        
        if recommendations:
            print("\n--- РЕКОМЕНДАЦИИ (на основе ваших предпочтений) ---")
            self.show_books(recommendations)

    def show_books(self, book_list=None):
        """Просмотр списка книг с сортировкой и фильтрацией"""
        if book_list is None:
            # Если это основной просмотр, предложим сортировку
            print("\nОпции просмотра: 1-Сортировка по названию, 2-По автору, 3-По году, 4-Фильтр по жанру, 0-Без всего")
            opt = input("Выбор: ")
            
            display_list = list(self.books)
            if opt == '1': display_list.sort(key=lambda x: x.title.lower())
            elif opt == '2': display_list.sort(key=lambda x: x.author.lower())
            elif opt == '3': display_list.sort(key=lambda x: x.year)
            elif opt == '4':
                g = input("Введите жанр для фильтрации: ").lower()
                display_list = [b for b in display_list if b.genre.lower() == g]
        else:
            display_list = book_list

        if not display_list:
            print("Список пуст.")
            return

        print(f"\n{'ID':<3} | {'Название':<25} | {'Автор':<20} | {'Жанр':<15} | {'Год':<5} | {'Статус'}")
        print("-" * 85)
        for i, b in enumerate(display_list):
            status = "✓ Прочитано" if b.is_read else "  Не прочитано"
            fav_mark = "★" if b.is_favorite else " "
            print(f"{i:<3} | {b.title[:25]:<25} | {b.author[:20]:<20} | {b.genre[:15]:<15} | {b.year:<5} | {status} {fav_mark}")

def main():
    library = Library()
    
    while True:
        print("\n" + "="*20)
        print("   Т-БИБЛИОТЕКА")
        print("="*20)
        print("1. Список всех книг")
        print("2. Добавить книгу")
        print("3. Поиск")
        print("4. Изменить статус / Избранное")
        print("5. Избранное и Рекомендации")
        print("6. Удалить книгу")
        print("0. Выход")
        
        choice = input("\nВыберите пункт меню: ")

        if choice == '1':
            library.show_books()
        elif choice == '2':
            library.add_book()
        elif choice == '3':
            library.search_books()
        elif choice == '4':
            library.change_status()
        elif choice == '5':
            library.get_favorites_and_recs()
        elif choice == '6':
            library.delete_book()
        elif choice == '0':
            print("Завершение работы...")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
