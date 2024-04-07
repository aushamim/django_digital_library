from django.shortcuts import render

from books.models import Book, Review
from categories.models import Category
from user_profile.models import Credits


def home(request, category_slug=None):
    categories = Category.objects.all()
    books = Book.objects.all()
    credits = None
    if request.user.is_authenticated:
        credits = Credits.objects.get(user=request.user)
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        books = Book.objects.filter(categories=category)
    return render(
        request,
        "home.html",
        {
            "user": request.user,
            "credits": credits,
            "categories": categories,
            "books": books,
        },
    )
