from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'books'

router = DefaultRouter()
router.register('all', views.BookAPIView, basename='all-books')
router.register('requested-books', views.RequestedBookAPIView, basename='requested_books')
router.register('matching', views.MatchingBookAPIView, basename='matching-books'),

urlpatterns = [
    path('', include(router.urls)),
]