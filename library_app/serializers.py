from rest_framework import serializers
from .models import Book, Author
from .validators import validate_publication_year, validate_book_uniqueness

#Сериалайзер который будем юзать в вьюс
class AuthorSerializer(serializers.ModelSerializer):

    #вычисляем колво книг с помощью метода гет букс каунт
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'name', 'biography', 'birth_date', 'died_date',
            'books_count'
        ]
        read_only_fields = ['id', 'books_count']

    def get_books_count(self, obj):
        return obj.books.count()


class BookSerializer(serializers.ModelSerializer):

    #берем имя автора из связанной модели Автор
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_name', 'publication_year',
            'genre', 'category', 'publisher', 'cover_image',
            'book_file', 'description'
        ]
        read_only_fields = ['id', 'author_name']

    #вызывается когда приходит поле публикайшен йер
    def validate_publication_year(self, value):
        return validate_publication_year(value)

    #При создании книги инстанс нон, при обновлении селф (если у селф есть атрибут инстанс(книга существует и мы ее обновляем)
    #то берем значение инстанса, если не существует, то нон
    def validate(self, data):
        return validate_book_uniqueness(data, instance=getattr(self, 'instance', None))