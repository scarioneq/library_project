from django.db import models

#Модель автора
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
