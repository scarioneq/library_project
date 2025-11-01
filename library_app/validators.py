from rest_framework import serializers
from .models import Book

#ПЕРЕПИСАТЬ МБ НА СВИЧКЕЙС
#придумать что делать с категорией худ.литра

#Функция, валидирующая год публикации
#!улучшить чтобы вместо 2025 был текущий год!
def validate_publication_year(value):
    if (value < 0) | value > 2025:
        raise serializers.ValidationError("Год публикации должен быть между 0 и 2025.")
    return value

#валидация уникальности книги в зависимости от категории
def validate_book_uniqueness(data, instance=None):
    title = data.get('title')
    author = data.get('author')
    publication_year = data.get('publication_year')
    publisher = data.get('publisher')
    category = data.get('category')

    #!после создания апи и тестирования проверю правильно ли это работает как я думаю, если че перепишу!
    #!Мб надо будет сделать так, чтобы в список попадали данные из instance!
    if not all([title, author, publication_year, publisher, category]):
        return data

    #Собираем все учебники из базы с одинаковыми полями названия, автора и издательства
    if category == 'textbook':
        existing_books = Book.objects.filter(
            title=title,
            author=author,
            publisher=publisher,
            category='textbook'
        )


        #Исключаем из результата self книгу при обновлении. Если этой штуки не будет то мы всегда будем натыкаться на ошибку валидации
        #при обновлении какой-то книги, ведь книга, которую мы обновляем уже есть в базе данных
        if instance:
            existing_books = existing_books.exclude(pk=instance.pk)

        #!это исключение оставляем!
        #Если после всех ифок у нас остались книги, значит это дубликат и выбрасываем исключение
        if existing_books.exists():
            raise serializers.ValidationError({
                'non_field_errors': [
                    'Учебник с таким названием, автором и издательством уже существует. '
                    'Можно добавлять только переиздания с разными годами публикации.'
                ]
            })

    return data