from rest_framework import serializers
from . models import Book, RequestedBook


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','category','title','author', 'slug','owner','available_now','city','country','contact_number','contact_email')
    

class RequestedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedBook
        fields = ('id','book', 'book_title','book_owner', 'requested_user','requested_user_name', 'contact_number','contact_email')

        
    