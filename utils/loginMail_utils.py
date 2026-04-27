from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


def _get_base_url():
    return getattr(settings, "SITE_BASE_URL", "https://sjtechsolution.pythonanywhere.com").rstrip("/")


def send_account_email(to_email: str, name: str, username: str, password: str, extra_context: dict = None):
    subject = "Your SG.Automix Tech Account is Ready!"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER)
    base_url = _get_base_url()
    login_url = f"{base_url}{reverse('login')}"

    context = {
        "name": name,
        "username": username,
        "password": password,
        "login_url": login_url,
        "logo_url": f"{base_url}/static/assets/images/SGAutomixTech_Black_bg_SizeFix.gif",
        **(extra_context or {}),
    }

    html_message = render_to_string("emails/account_created.html", context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=f"Your account has been created. Login here: {login_url}",
        from_email=from_email,
        to=[to_email],
    )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
