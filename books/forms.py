from django import forms

from books.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]
