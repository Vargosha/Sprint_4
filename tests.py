import pytest
from main import BooksCollector

class TestBooksCollector:

    @pytest.mark.parametrize('book_name, expected_in_collection', [
        ('', False), #0 символов
        ('А', True), #1 символ
        ('Тайна забытого ключа', True), #20 символов
        ('Тайна ледяного озера или Забытый дневник', True), #40 символов
        ('Замок на краю света или пропавшая комната', False), #41 символ
        ('Призрачный огонь незабвенной памяти или Як', False) #42 символа
        ])
    def test_add_new_book_accepts_only_names_within_length_limit(self, book_name, expected_in_collection):
        collector = BooksCollector()

        collector.add_new_book(book_name)

        if expected_in_collection:
            assert book_name in collector.get_books_genre()
        else:
            assert book_name not in collector.get_books_genre()

    def test_add_new_book_does_not_add_already_existing_book(self):
        collector = BooksCollector()

        collector.add_new_book('Тайна забытого ключа')
        collector.add_new_book('Тайна забытого ключа') #дубликат

        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_adds_books_with_empty_genre(self):
        collector = BooksCollector()
        expected_result = {'Тайна забытого ключа': '', 'Тайна забытой книги': ''} #книга добавляется без жанра

        collector.add_new_book('Тайна забытого ключа')
        collector.add_new_book('Тайна забытой книги')

        assert collector.get_books_genre() == expected_result

    @pytest.mark.parametrize('book_name, book_genre, expected_genre', [
        ('Тайна забытого ключа', 'Фантастика', 'Фантастика'), #сущ. книга и сущ. жанр
        ('Тайна ледяного озера или Забытый дневник', 'Ужасы', None), #несущ. книга и сущ. жанр
        ('Тайна забытой книги', 'Боевик', '') #сущ. книга и несущ. жанр
        ])
    def test_set_book_genre_works_only_for_existing_books_and_valid_genres(self, book_name, book_genre, expected_genre):
        collector = BooksCollector()

        collector.add_new_book('Тайна забытого ключа')
        collector.add_new_book('Тайна забытой книги')
        collector.set_book_genre(book_name, book_genre)

        assert collector.get_book_genre(book_name) == expected_genre

    @pytest.mark.parametrize('book_name, expected_genre', [
        ('Тайна забытого ключа', 'Фантастика'), #сущ. книга с жанром
        ('Тайна забытой книги', ''), #сущ. книга без жанра
        ('Тайна ледяного озера или Забытый дневник', None) #несущ. книга
        ])
    def test_get_book_genre_returns_correct_genre_for_all_input_types(self, book_name, expected_genre):
        collector = BooksCollector()

        collector.add_new_book('Тайна забытого ключа')
        collector.add_new_book('Тайна забытой книги')
        collector.set_book_genre('Тайна забытого ключа', 'Фантастика')

        assert collector.get_book_genre(book_name) == expected_genre

    @pytest.mark.parametrize('genre, expected_in_list', [
        ('Фантастика', True), #сущ. жанр
        ('Боевик', False) #несущ. жанр
        ])
    def test_get_books_with_specific_genre_returns_correct_list_for_valid_and_invalid_genres(self, genre, expected_in_list):
        collector = BooksCollector()

        collector.add_new_book('Тайна забытого ключа')
        collector.add_new_book('Тайна забытой книги')
        collector.set_book_genre('Тайна забытого ключа', 'Фантастика')
        collector.set_book_genre('Тайна забытой книги', 'Фантастика')

        if expected_in_list:
            assert len(collector.get_books_with_specific_genre(genre)) == 2
        else:
            assert len(collector.get_books_with_specific_genre(genre)) == 0

    def test_get_books_genre_returns_full_dictionary(self):
        collector = BooksCollector()
        expexted_result = {'Тайна забытого ключа': 'Фантастика', 'Тайна забытой книги': ''}

        collector.add_new_book('Тайна забытого ключа') #книга с жанром
        collector.add_new_book('Тайна забытой книги') #книга без жанра
        collector.set_book_genre('Тайна забытого ключа', 'Фантастика')

        assert collector.get_books_genre() == expexted_result

    def test_get_books_for_children_returns_only_child_friendly_books(self):
        collector = BooksCollector()
        expected_result = ['Тайна забытого ключа']

        collector.add_new_book('Тайна забытого ключа') #книга с жанром без возрастного рейтинга
        collector.add_new_book('Тайна забытой книги') #книга без жанра
        collector.add_new_book('Детские ужасы') #книга с жанром с возрастным рейтингом
        collector.set_book_genre('Тайна забытого ключа', 'Фантастика')
        collector.set_book_genre('Детские ужасы', 'Ужасы')

        assert collector.get_books_for_children() == expected_result

    @pytest.mark.parametrize('book_name, expected_in_list', [
        ('Тайна забытого ключа', True),  # сущ. книга
        ('Тайна забытой книги', False)  # несущ. книга
    ])
    def test_add_book_in_favorites_works_only_for_existing_books(self, book_name, expected_in_list):
        collector = BooksCollector()

        collector.add_new_book('Тайна забытого ключа')
        collector.add_book_in_favorites(book_name)

        if expected_in_list:
            assert book_name in collector.get_list_of_favorites_books()
        else:
            assert book_name not in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_does_not_add_already_existing_book(self):
        collector = BooksCollector()

        collector.add_new_book('Тайна забытого ключа')
        collector.add_book_in_favorites('Тайна забытого ключа')
        collector.add_book_in_favorites('Тайна забытого ключа') #дубликат

        assert len(collector.get_list_of_favorites_books()) == 1

    @pytest.mark.parametrize('book_name', [
        'Тайна забытого ключа', #книга в избранном
        'Тайна забытой книги' #книга не в избранном
        ])
    def test_delete_book_from_favorites_removes_book_successfully(self, book_name):
        collector = BooksCollector()

        collector.add_new_book('Тайна забытого ключа')
        collector.add_new_book('Тайна забытой книги')
        collector.add_book_in_favorites('Тайна забытого ключа')
        collector.delete_book_from_favorites(book_name)

        assert book_name not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_returns_full_list(self):
        collector = BooksCollector()
        expected_result = ['Тайна забытого ключа', 'Тайна забытой книги']

        collector.add_new_book('Тайна забытого ключа')
        collector.add_new_book('Тайна забытой книги')
        collector.add_book_in_favorites('Тайна забытого ключа')
        collector.add_book_in_favorites('Тайна забытой книги')

        assert collector.get_list_of_favorites_books() == expected_result
