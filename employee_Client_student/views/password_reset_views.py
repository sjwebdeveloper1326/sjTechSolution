from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        return super().form_valid(form)


class CustomPasswordResetView(auth_views.PasswordResetView):

    template_name = "auth/password_reset.html"
    email_template_name = "emails/password_reset_email.html"
    html_email_template_name = "emails/password_reset_email.html"
    subject_template_name = "emails/password_reset_subject.txt"

    def form_valid(self, form):

        email = form.cleaned_data.get("email")

        try:
            user = User.objects.get(email=email)

            if user.is_superuser:
                messages.error(
                    self.request,
                    "Password reset is not allowed for this account."
                )
                return redirect("password_reset")

            messages.success(
                self.request,
                "Password reset link has been sent to your email address."
            )

        except User.DoesNotExist:

            messages.error(
                self.request,
                "No account found with this email address."
            )

            return redirect("password_reset")

        except Exception:

            messages.error(
                self.request,
                "Something went wrong. Please try again."
            )

            return redirect("password_reset")

        return super().form_valid(form)


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):

    def get(self, request, *args, **kwargs):

        messages.success(
            request,
            "Your password has been reset successfully. Please login with your new password."
        )

        return redirect("login")


def register_view(request):
    return render(request, "auth/register.html")