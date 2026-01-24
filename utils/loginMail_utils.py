# # project/utils/mail_utils.py
# from django.core.mail import send_mail
# from django.conf import settings
# from django.template.loader import render_to_string

# def send_account_email(to_email: str, name: str, username: str, password: str, extra_context: dict = None):
#     """
#     Send account creation email. Uses Django send_mail.
#     You can replace message with render_to_string() and an HTML template if needed.
#     """
#     subject = "🎉 Your SJ.Tech Solution Account Created"
#     # plain text message
#     message = (
#         f"Hello {name},\n\n"
#         f"Your account has been created successfully.\n\n"
#         f"Username: {username}\n"
#         f"Password: {password}\n\n"
#         f"Please login and change your password after first login.\n\n"
#         f"Regards,\nSJ.Tech Solution\n"
#     )

#     # If you want HTML, you can render a template:
#     # html_message = render_to_string('emails/account_created.html', context)
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER),
#         recipient_list=[to_email],
#         fail_silently=False,  # you can set True in production if you prefer
#     )


# project/utils/mail_utils.py

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

def send_account_email(to_email: str, name: str, username: str, password: str, extra_context: dict = None):
    subject = "🎉 Your SJ.Tech Solution Account is Ready!"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER)

    context = {
        'name': name,
        'username': username,
        'password': password,
        **(extra_context or {})
    }

    html_message = render_to_string('emails/account_created.html', context)

    email = EmailMultiAlternatives(
        subject=subject,
        body="Your account has been created. Login here: https://yoursite.com/login",  # fallback plain text
        from_email=from_email,
        to=[to_email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)