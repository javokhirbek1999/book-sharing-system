from django.contrib import admin

from . import models

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','slug')
    prepopulated_fields = {'slug':('title',),}

admin.site.register(models.Category)
admin.site.register(models.RequestedBook)