from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .forms import CustomUserCreationForm,CustomAuthenticationForm,ProfileForm
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.urls import reverse_lazy, reverse
from .models import Profile
from django.contrib.auth import login
from .mixins import VerifiedRequiredMixin
# Create your views here.

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:home')
    def form_valid(self, form):
        to_return = super().form_valid(form)
        messages.success(self.request, "Registration successful")

        login(self.request, self.object)
        return to_return



class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy("core:home")
    def form_valid(self, form):
        messages.success(self.request, "You are logged in")
        return super().form_valid(form)


class LogoutConfirmView(TemplateView):
    template_name = "registration/logged_out.html"



class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy(
        "accounts:password_reset_done"
    )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy(
        "accounts:password_reset_complete"
    )




class ProfileView(LoginRequiredMixin,VerifiedRequiredMixin,DetailView):
    template_name = "accounts/profile.html"
    model = Profile
    context_object_name = "profile"
    def get_queryset(self):
        return Profile.objects.filter(
            user=self.request.user
        )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verified:
            messages.error(
                request,
                "You are not verified"
            )
            return redirect("core:home")

        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin,UpdateView):
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
            kwargs={"pk": self.object.pk}
        )
    def form_valid(self, form):
        messages.success(self.request, "Profile updated")
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")

class PasswordChangeConfirmView(LoginRequiredMixin,TemplateView):
    template_name = "registration/password_change_done.html"

