import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

# from employee_Client_student.models import Employee, Student

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        return super().form_valid(form)


# password reset email send hone ke baad SUCCESS MESSAGE ke liye
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset.html'
    email_template_name = 'emails/password_reset_email.html'
    html_email_template_name = 'emails/password_reset_email.html'
    subject_template_name = 'emails/password_reset_subject.txt'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        # superadmin check
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
            if user.is_superuser:
                messages.error(
                    self.request,
                    "You can change password of this mail from hare!."
                )
                return redirect('password_reset')
        except User.DoesNotExist:
            pass

        messages.success(
            self.request,
            "Password reset link aapke email par bhej diya gaya hai."
        )
        return super().form_valid(form)



# passwod change start...

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Your password has been reset successfully! Please login again.")
        return redirect('login')   # ← yaha apne login URL ka name daalna

# passwod change end...

def register_view(request):
    return render(request, "auth/register.html")