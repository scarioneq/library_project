from rest_framework import serializers
from .models import Book


def validate_publication_year(value):
    if (value < 0) | (value > 2025):
        raise serializers.ValidationError("Год публикации должен быть между 0 и 2025.")
    return value


#Логика валидации:
#Для худ литры и других категорий запрещаем только дубликаты по тайтл, автор, год, издательство (это сделано на уровне модели)
#Для учебников запрещаем дубликаты по издательству, если уже есть учебник с названием и автором
#Разрешаем создавать только учебники с разными годами публикации

def validate_book_uniqueness(data, instance=None):
    title = data.get('title')
    author = data.get('author')
    publisher = data.get('publisher')
    category = data.get('category')


    #Логика для учебников
    if category == 'textbook':
        #Запрещаем создавать учебники с другим издательством, если уже есть учебник с таким тайлом и автором
        existing_textbooks_same_title_author = Book.objects.filter(
            title=title,
            author=author,
            category='textbook'
        )

        #Если обновляем сущ. учебник, исключаем проверки для нее
        if instance:
            existing_textbooks_same_title_author = existing_textbooks_same_title_author.exclude(pk=instance.pk)

        #Если нашли учебники с таким же названием и автором
        if existing_textbooks_same_title_author.exists():
            #Получаем все издательства этих учебников
            existing_publishers = set(existing_textbooks_same_title_author.values_list('publisher', flat=True))

            #Если пытаемся создать с издательством, которого нет в существующих выдаем ошибку
            if publisher not in existing_publishers:
                raise serializers.ValidationError({
                    'publisher': [
                        f'Нельзя создавать учебник с другим издательством. '
                        f'Для учебника "{title}" автора {author.name} уже установлено издательство: {", ".join(existing_publishers)}. '
                        f'Можно создавать только переиздания с разными годами публикации.'
                    ]
                })

    return data