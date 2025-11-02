from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
#для фильтров книг добавили библу неплохую
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author
from .serializers import BookSerializer, AuthorSerializer
from .permissions import IsAdminOrReadOnly

#вьюсет с встроенным крудом
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    #теперь можем искать авторов с помощью параметра search
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    #дополнение для круда авторов, чтобы можно было искать все книги конкретного автора
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        author = self.get_object()
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)