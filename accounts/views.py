from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView as DjangoPasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    ProfileForm,
)
from .mixins import VerifiedRequiredMixin
from .models import Profile
from .services import send_activation_email


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)

        send_activation_email(self.object)

        messages.success(
            self.request,
            "Registration successful. Please check your email to activate your account.",
        )

        return response


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        messages.success(
            self.request,
            "You are logged in",
        )
        return super().form_valid(form)


class LogoutConfirmView(TemplateView):
    template_name = "registration/logged_out.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")


class ProfileView(
    LoginRequiredMixin,
    VerifiedRequiredMixin,
    DetailView,
):
    template_name = "accounts/profile.html"
    model = Profile
    context_object_name = "profile"

    def get_queryset(self):
        return Profile.objects.filter(
            user=self.request.user
        )


class ProfileUpdateView(
    LoginRequiredMixin,
    VerifiedRequiredMixin,
    UpdateView,
):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"

    def get_queryset(self):
        return Profile.objects.filter(
            user=self.request.user
        )

    def get_success_url(self):
        return reverse(
            "accounts:profile",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Profile updated",
        )
        return super().form_valid(form)


class PasswordChangeView(
    LoginRequiredMixin,
    DjangoPasswordChangeView,
):
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")


class PasswordChangeConfirmView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = "registration/password_change_done.html"