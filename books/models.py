from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):

    class AvailableBooks(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(available_now=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, default="")
    available_now = models.BooleanField(default=False)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    contact_number = models.CharField(max_length=200, null=True)
    contact_email = models.CharField(max_length=200, null=False)

    objects = models.Manager()
    available_books = AvailableBooks()

    def __str__(self):
        return self.title


class RequestedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requested_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=200, null=True)
    contact_email = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.book.title
    
    @property
    def requested_user_name(self):
        return self.requested_user.name

    @property
    def book_owner(self):
        return self.book.owner.name

    @property
    def book_title(self):
        return self.book.title
    
    
