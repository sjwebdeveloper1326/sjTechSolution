from django.contrib import messages
from django.shortcuts import redirect, render

from employee_Client_student.models.student_model import Student
from mainApp.models.course_model import Course
from mainApp.models.payment_model import Payment

from django.contrib import messages

def submit_payment(request, course_id):

    course = Course.objects.get(id=course_id)

    if request.method == "POST":

        student = Student.objects.get(user=request.user)

        amount = request.POST.get("amount")
        message = request.POST.get("message")
        screenshot = request.FILES.get("payment_screenshot")

        Payment.objects.create(
            student=student,
            course=course,
            amount=amount,
            message=message,
            screenshot=screenshot
        )

        messages.success(
            request,
            "Payment submitted successfully. Within 24 hours your payment will be confirmed."
        )

        return redirect("student_dashboard")

    return render(request, "partials/payment_form.html", {
        "course": course
    })