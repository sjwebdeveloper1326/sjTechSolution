import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from employee_Client_student.models import Student
from utils.date_context import build_date_context
from utils.site_urls import absolute_url

logger = logging.getLogger(__name__)

def send_new_course_email(course):
    students = Student.objects.exclude(email="")
    courses_url = absolute_url(reverse('courses'))

    for student in students:
        try:
            context = {
                "name": student.name,
                "course_title": course.title,
                "course_description": course.description,
                "site_url": courses_url,
                **build_date_context(),
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
