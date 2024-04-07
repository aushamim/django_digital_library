from django.db import models
from django.contrib.auth.models import User

from categories.models import Category


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    categories = models.ManyToManyField(Category)
    image = models.ImageField(upload_to="books/")

    def __str__(self):
        return self.title


class BorrowRecords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    balance_after_borrowing = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.book.title}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"
