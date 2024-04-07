from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from books.models import BorrowRecords
from user_profile.forms import CreditsForm, SignUpForm
from user_profile.models import Credits


# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "user_creation_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)

        Credits.objects.create(user=self.object, credit=0)

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Account Created and Logged in Successfully")
        else:
            messages.error(self.request, "Login Failed")

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create an account"
        return context


class Login(LoginView):
    template_name = "user_creation_form.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Logged In Successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Please Login"
        return context


class Logout(LogoutView):

    def get_success_url(self):
        messages.success(self.request, "Logged Out Successfully")
        return redirect("home")


class AddCreditsView(LoginRequiredMixin, CreateView):
    model = Credits
    form_class = CreditsForm
    template_name = "user_creation_form.html"

    def form_valid(self, form):
        user_credits = Credits.objects.get(user=self.request.user)
        amount = form.cleaned_data["credit"]
        user_credits.credit += amount
        user_credits.save()

        messages.success(self.request, f"Successfully added {amount} credits")

        message = render_to_string(
            "add_credits_email.html",
            {
                "user": self.request.user,
                "amount": amount,
                "new_amount": user_credits.credit,
            },
        )
        send_email = EmailMultiAlternatives(
            "Add Credits", "", to=[self.request.user.email]
        )
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        return redirect("home")


@login_required
def Profile(request):
    borrowed_records = BorrowRecords.objects.filter(user=request.user)
    return render(
        request,
        "profile.html",
        {"user": request.user, "borrowed_records": borrowed_records},
    )
