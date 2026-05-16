from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from mainApp.forms import TestimonialForm
from mainApp.models import Testimonial
from employee_Client_student.decorators import admin_level_required
from utils.site_urls import absolute_url


# def _get_superadmin_emails():
#     user_model = get_user_model()
#     emails = list(
#         user_model.objects.filter(is_superuser=True)
#         .exclude(email="")
#         .values_list("email", flat=True)
#     )
#     if not emails and getattr(settings, "EMAIL_HOST_ADMIN", ""):
#         emails = [settings.EMAIL_HOST_ADMIN]
#     return emails
def _get_admin_emails():
    emails = []

    # ENV Email
    env_email = getattr(settings, "EMAIL_HOST_ADMIN", "")

    if env_email:
        emails.append(env_email)

    # print("📧 Admin Emails:", emails)

    return emails


def _send_testimonial_approval_email(request, testimonial):
    recipients = _get_admin_emails()
    if not recipients:
        return False

    token = signing.dumps(
        {"testimonial_id": testimonial.id}, salt="testimonial-approval")
    approve_link = absolute_url(
        reverse("testimonial_accept_from_email", kwargs={"token": token}),
        request,
    )

    subject = f"New testimonial approval request: {testimonial.name}"
    message = (
        "A new testimonial is waiting for approval.\n\n"
        f"Name: {testimonial.name}\n"
        f"Designation: {testimonial.designation}\n"
        f"Email: {testimonial.email}\n"
        f"Rating: {testimonial.rating}\n\n"
        f"Message:\n{testimonial.message}\n\n"
        f"Approve from email:\n{approve_link}\n"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL",
                           settings.EMAIL_HOST_USER),
        recipient_list=recipients,
        fail_silently=False,
    )
    return True


@admin_level_required
def testimonial_list(request):
    queryset = Testimonial.objects.all().order_by("-id")
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get("page")
    testimonials = paginator.get_page(page_number)
    return render(request, "testimonialCRUD/testimonial_list.html", {"testimonials": testimonials})


def add_testimonial(request, slug=None):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.isaccepted = False
            testimonial.save()

            try:
                mail_sent = _send_testimonial_approval_email(
                    request, testimonial)
                if mail_sent:
                    messages.success(
                        request,
                        "Testimonial submitted. It will be visible after admin approval.",
                    )
                else:
                    messages.warning(
                        request,
                        "Testimonial saved but admin email is not configured.",
                    )
            except Exception:
                messages.warning(
                    request,
                    "Testimonial saved, but approval email could not be sent.",
                )

            if request.user.is_authenticated:
                return redirect("testimonial_list")
            return redirect("testimonial")

        messages.error(request, "Please fix the form errors.")
    else:
        form = TestimonialForm()

    return render(request, "testimonialCRUD/testimonial_form.html", {"form": form})


@admin_level_required
def edit_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    if request.method == "POST":
        form = TestimonialForm(
            request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully.")
            return redirect("testimonial_list")
        messages.error(request, "Please fix the form errors.")
    else:
        form = TestimonialForm(instance=testimonial)

    return render(request, "testimonialCRUD/testimonial_form.html", {"form": form})


@admin_level_required
def delete_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.delete()
    messages.success(request, "Testimonial deleted successfully.")
    return redirect("testimonial_list")


@admin_level_required
def accept_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    if testimonial.isaccepted:
        messages.info(request, "Testimonial is already accepted.")
    else:
        testimonial.isaccepted = True
        testimonial.save(update_fields=["isaccepted"])
        messages.success(request, "Testimonial accepted successfully.")
    return redirect("testimonial_list")


def accept_testimonial_from_email(request, token):
    try:
        data = signing.loads(
            token, salt="testimonial-approval", max_age=60 * 60 * 24 * 7)
        testimonial = get_object_or_404(Testimonial, id=data["testimonial_id"])
    except signing.BadSignature:
        messages.error(request, "Approval link is invalid or expired.")
        return redirect("testimonial")

    if testimonial.isaccepted:
        messages.info(request, "Testimonial is already accepted.")
    else:
        testimonial.isaccepted = True
        testimonial.save(update_fields=["isaccepted"])
        messages.success(request, "Testimonial approved from email link.")
    return redirect("testimonial")
