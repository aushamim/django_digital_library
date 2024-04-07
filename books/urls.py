from django.urls import path

from books.views import (
    BookDetails,
    BorrowBookView,
    ReturnBookView,
    ReviewFullView,
    ReviewView,
)


urlpatterns = [
    path("details/<int:id>", BookDetails.as_view(), name="details"),
    path("borrow/<int:id>", BorrowBookView.as_view(), name="borrow"),
    path("return/<int:id>", ReturnBookView.as_view(), name="return"),
    path("review/<int:id>", ReviewView.as_view(), name="review"),
    path("review-full/<int:id>", ReviewFullView, name="review_full"),
]
