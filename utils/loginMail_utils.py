from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def send_account_email(to_email: str, name: str, username: str, password: str, extra_context: dict = None):

    subject = "🎉 Your SG.Automix Tech Account is Ready!"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER)

    context = {
        'name': name,
        'username': username,
        'password': password,
        'protocol': 'https',
        'domain': 'sjtechsolution.pythonanywhere.com',
        'logo_url': 'https://sjtechsolution.pythonanywhere.com/static/assets/images/SGAutomixTech_Black_bg_SizeFix.gif',
        **(extra_context or {})
    }

    html_message = render_to_string('emails/account_created.html', context)
    print("Generated HTML email content:",context)
    email = EmailMultiAlternatives(
        subject=subject,
        body="Your account has been created. Login here: https://sjtechsolution.pythonanywhere.com/login",
        from_email=from_email,
        to=[to_email]
    )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)