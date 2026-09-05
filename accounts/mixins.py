from django.contrib import messages
from django.shortcuts import redirect


class VerifiedRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verified:
            messages.error(request, "You are not verified")
            return redirect("core:home")

        return super().dispatch(request, *args, **kwargs)
