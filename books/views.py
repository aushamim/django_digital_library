from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, CreateView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from books.forms import ReviewForm
from books.models import Book, BorrowRecords, Review
from user_profile.models import Credits


# Create your views here.
class BookDetails(DetailView):
    model = Book
    pk_url_kwarg = "id"
    template_name = "book_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(id=self.kwargs["id"])
        reviews = Review.objects.filter(book=book)
        context["title"] = "Book Details"
        context["reviews"] = reviews
        return context


class BorrowBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        credits = Credits.objects.get(user=self.request.user)

        if credits.credit < book.price:
            messages.error(
                self.request,
                f"You don't have enough credits to borrow '{book.title}'. Please add credits to borrow this book.",
            )
            return redirect("home")

        credits.credit -= book.price
        credits.save()

        borrow_record = BorrowRecords.objects.create(
            user=self.request.user,
            book=book,
            balance_after_borrowing=credits.credit,
        )

        messages.success(self.request, f"Successfully borrowed '{book.title}'.")

        message = render_to_string(
            "book_borrowed_email.html",
            {"user": self.request.user, "borrow_record": borrow_record},
        )
        send_email = EmailMultiAlternatives(
            "Borrowed Book", "", to=[self.request.user.email]
        )
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        return redirect("profile")


class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        record = get_object_or_404(BorrowRecords, id=id)

        if record.returned == True:
            messages.error(
                self.request, f"You have already returned '{record.book.title}'."
            )
            return redirect("profile")

        credits = Credits.objects.get(user=self.request.user)
        credits.credit += record.book.price
        credits.save()

        record.returned = True
        record.save()

        messages.success(self.request, f"Successfully returned '{record.book.title}'.")

        message = render_to_string(
            "book_returned_email.html",
            {"user": self.request.user, "borrow_record": record},
        )
        send_email = EmailMultiAlternatives(
            "Returned Book", "", to=[self.request.user.email]
        )
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        return redirect("profile")


class ReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review.html"
    pk_url_kwarg = "id"

    def form_valid(self, form):
        book = Book.objects.get(id=self.kwargs["id"])

        review_instance = form.save(commit=False)
        review_instance.user = self.request.user
        review_instance.book = book
        review_instance.save()

        messages.success(self.request, f"Successfully added review for '{book.title}'")
        return redirect("profile")

    def get_context_data(self, **kwargs):
        book = Book.objects.get(id=self.kwargs["id"])
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Review"
        context["book"] = book
        return context


def ReviewFullView(request, id):
    review = Review.objects.get(id=id)
    return render(request, "review_full.html", {"title": "Review", "review": review})
