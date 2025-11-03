from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
#для фильтров книг добавили библу неплохую
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
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


#круд для книг
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('author').order_by('title')
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'genre', 'author__name']
    filterset_fields = ['category', 'author', 'publication_year', 'publisher']

    #кастомный метод к круду, который создает эндпоинт для поиска
    @action(detail=False, methods=['get'])
    def search_advanced(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        title = request.query_params.get('title', None)
        author_name = request.query_params.get('author_name', None)
        genre = request.query_params.get('genre', None)
        category = request.query_params.get('category', None)
        year_from = request.query_params.get('year_from', None)
        year_to = request.query_params.get('year_to', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if category:
            queryset = queryset.filter(category=category)
        if year_from:
            queryset = queryset.filter(publication_year__gte=year_from)
        if year_to:
            queryset = queryset.filter(publication_year__lte=year_to)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)