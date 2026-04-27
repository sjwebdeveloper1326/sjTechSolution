import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from employee_Client_student.models import Student

logger = logging.getLogger(__name__)


def _get_base_url():
    return getattr(settings, "SITE_BASE_URL", "https://sjtechsolution.pythonanywhere.com").rstrip("/")


def send_new_course_email(course):
    students = Student.objects.exclude(email="")
    base_url = _get_base_url()
    courses_url = f"{base_url}{reverse('courses')}"

    for student in students:
        try:
            context = {
                "name": student.name,
                "course_title": course.title,
                "course_description": course.description,
                "site_url": courses_url,
            }

            html_content = render_to_string("emails/new_course_email.html", context)

            email = EmailMultiAlternatives(
                subject=f"New Course: {course.title}",
                body=f"New course available. View it here: {courses_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[student.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            logger.error(f"Email failed for {student.email}: {e}")
