from django.contrib import admin

from books.models import Book, BorrowRecords, Review

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(BorrowRecords)
