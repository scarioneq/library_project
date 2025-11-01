from django.db import models

#Модель автора (представление сущности в базе данных)
class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    died_date = models.DateField(null=True, blank=True)

    #Представление в админке джанго
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    #Метод, возвращающий строковое представление
    def __str__(self):
        return self.name

#Модель книги (представление сущности в базе данных)
class Book(models.Model):
    BOOK_CATEGORIES = [
        ('fiction', 'Художественная литература'),
        ('textbook', 'Учебник'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=BOOK_CATEGORIES)
    publisher = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    book_file = models.FileField(upload_to='books/', null=True, blank=True)
    description = models.TextField(blank=True)

    #Представление в админке джанго
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

        #Уникальность полей
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'publication_year', 'publisher'],
                name='unique_book'
            )
        ]

    #Строкое представление с форматированной строкой
    def __str__(self):
        return f"{self.title} - {self.author.name}"