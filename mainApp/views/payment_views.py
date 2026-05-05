# from django.contrib import messages
# from django.shortcuts import redirect, render

# from employee_Client_student.models.student_model import Student
# from mainApp.models.course_model import Course
# from mainApp.models.payment_model import Payment


# def submit_payment(request, course_id):

#     course = Course.objects.get(id=course_id)

#     try:
#         student = Student.objects.get(user=request.user)
#     except Student.DoesNotExist:
#         messages.error(request, "Student profile not found.")
#         return redirect("student_dashboard")

#     # 🚫 Stop duplicate payment
#     if Payment.objects.filter(student=student, course=course).exists():
#         messages.warning(request, "You already submitted payment for this course.")
#         return redirect("dashboard_student", stu_uuid=student.stu_uuid)
    
#     if request.method == "POST":

#         amount = request.POST.get("amount")
#         message = request.POST.get("message")
#         screenshot = request.FILES.get("payment_screenshot")

#         if not screenshot:
#             messages.error(request, "Please upload payment screenshot.")
#             return redirect("submit_payment", course_id=course.id)

#         Payment.objects.create(
#             student=student,
#             course=course,
#             amount=amount,
#             message=message,
#             screenshot=screenshot
#         )

#         messages.success(
#             request,
#             "Payment submitted successfully. Within 24 hours your payment will be confirmed."
#         )

#         return redirect("student_dashboard")

#     return render(request, "partials/payment_form.html", {
#         "course": course
#     })

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from employee_Client_student.models.student_model import Student
from mainApp.models.course_model import Course
from mainApp.models.payment_model import Payment


@login_required(login_url="login")
def submit_payment(request, course_id):

    course = Course.objects.get(id=course_id)

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect("login")

    # 🚫 Stop duplicate payment
    if Payment.objects.filter(student=student, course=course).exists():
        messages.warning(request, "You already submitted payment for this course.")
        return redirect("dashboard_student", stu_uuid=student.stu_uuid)

    if request.method == "POST":

        amount = request.POST.get("amount")
        message = request.POST.get("message")
        screenshot = request.FILES.get("payment_screenshot")

        if not screenshot:
            messages.error(request, "Please upload payment screenshot.")
            return redirect("submit_payment", course_id=course.id)

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

        return redirect("dashboard_student", stu_uuid=student.stu_uuid)

    return render(request, "partials/payment_form.html", {
        "course": course
    })
