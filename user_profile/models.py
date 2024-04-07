from django.db import models
from django.contrib.auth.models import User

from books.models import Book


# Create your models here.
class Credits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.user.username}'s credits"
