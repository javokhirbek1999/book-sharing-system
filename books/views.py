from django.shortcuts import render
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

from .models import Book, RequestedBook
from .serializers import BookSerializer, RequestedBookSerializer
from .permissions import IsOwnerOrReadOnly
from .utils import Util


class BookAPIView(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = BookSerializer
    queryset = Book.available_books.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ['^slug']


    def get_object(self, queryset=None, **kwargs):
        slug = self.kwargs.get('pk')
        return Book.available_books.get(slug=slug)


class RequestedBookAPIView(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = RequestedBookSerializer
    queryset = RequestedBook.objects.all()
    filter_backends = [filters.SearchFilter]


    def get_object(self, queryset=None, **kwargs):
        slug = self.kwargs.get('pk')
        return RequestedBook.objects.filter(slug=slug)

class MatchingBookAPIView(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = RequestedBookSerializer
    filter_backends = [filters.SearchFilter]
    
    def get_queryset(self):
        return RequestedBook.objects.filter(requested_user=self.request.user)