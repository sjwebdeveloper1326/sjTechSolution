from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

# from mainApp.models import Course
from employee_Client_student.models import Employee
from employee_Client_student.decorators import admin_level_required


@admin_level_required
def course_list(request):
    courses = Course.objects.all().order_by('order', 'created_at')
    
    # Attach teacher names for display
    teachers = Employee.objects.filter(role="teacher")
    teacher_map = {str(t.emp_uuid): t for t in teachers}

    for course in courses:
        teacher_names = []
        if course.teacher_ids:
            for uuid_str in course.teacher_ids:
                teacher = teacher_map.get(uuid_str)
                if teacher:
                    teacher_names.append(f"{teacher.name} ({teacher.emp_id})")
        course.teacher_names = teacher_names

    return render(request, "courseCRUD/course_list.html", {
        "courses": courses
    })


from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from mainApp.models import Course
from employee_Client_student.models import Employee


@admin_level_required
def course_create(request):
    teachers = Employee.objects.filter(role="teacher").order_by("name")

    if request.method == "POST":
        try:
            title = request.POST.get("title", "").strip()
            subtitle = request.POST.get("subtitle", "").strip()
            description = request.POST.get("description", "").strip()
            order = int(request.POST.get("order", 0))
            is_new = request.POST.get("is_new") == "on"
            email_sent = request.POST.get("email_sent") == "on"

            # ─── New fields ───────────────────────────────────────
            price_str = request.POST.get("price", "0")
            discounted_price_str = request.POST.get("discounted_price", "")

            try:
                price = Decimal(price_str)
            except InvalidOperation:
                price = Decimal("0.00")

            discounted_price = None
            if discounted_price_str.strip():
                try:
                    discounted_price = Decimal(discounted_price_str)
                except InvalidOperation:
                    messages.warning(request, "Invalid discounted price format — saved as none.")

            duration_display = request.POST.get("duration_display", "").strip()

            # Features: textarea → split by comma or newline
            features_raw = request.POST.get("features", "").strip()
            features = [f.strip() for f in features_raw.replace("\n", ",").split(",") if f.strip()]

            teacher_uuids = request.POST.getlist("teacher_ids")  # already list of strings

            Course.objects.create(
                title=title,
                subtitle=subtitle,
                description=description,
                price=price,
                discounted_price=discounted_price,
                duration_display=duration_display,
                features=features,
                teacher_ids=teacher_uuids,
                order=order,
                is_new=is_new,
                email_sent=email_sent,
            )

            messages.success(request, "Course created successfully!")
            return redirect("course_list")

        except Exception as e:
            messages.error(request, f"Error creating course: {str(e)}")

    return render(request, "courseCRUD/course_form.html", {
        "teachers": teachers,
        "action": "Create"
    })


@admin_level_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    teachers = Employee.objects.filter(role="teacher").order_by("name")

    if request.method == "POST":
        try:
            course.title = request.POST.get("title", "").strip()
            course.subtitle = request.POST.get("subtitle", "").strip()
            course.description = request.POST.get("description", "").strip()
            course.order = int(request.POST.get("order", 0))
            course.is_new = request.POST.get("is_new") == "on"

            # ─── New fields ───────────────────────────────────────
            price_str = request.POST.get("price", "0")
            discounted_price_str = request.POST.get("discounted_price", "")

            try:
                course.price = Decimal(price_str)
            except InvalidOperation:
                course.price = Decimal("0.00")

            if discounted_price_str.strip():
                try:
                    course.discounted_price = Decimal(discounted_price_str)
                except InvalidOperation:
                    course.discounted_price = None
                    messages.warning(request, "Invalid discounted price — cleared.")
            else:
                course.discounted_price = None

            course.duration_display = request.POST.get("duration_display", "").strip()

            # Features
            features_raw = request.POST.get("features", "").strip()
            course.features = [f.strip() for f in features_raw.replace("\n", ",").split(",") if f.strip()]

            course.teacher_ids = request.POST.getlist("teacher_ids")

            course.save()

            messages.success(request, "Course updated successfully!")
            return redirect("course_list")

        except Exception as e:
            messages.error(request, f"Error updating course: {str(e)}")

    return render(request, "courseCRUD/course_form.html", {
        "course": course,
        "teachers": teachers,
        "action": "Update"
    })

@admin_level_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course_title = course.title
        course.delete()
        messages.success(request, f"Course '{course_title}' deleted successfully")
        return redirect("course_list")

    return render(request, "courseCRUD/course_delete.html", {"course": course})


# Frontend Courses Page
def courses_page(request):
    courses = Course.objects.all().order_by('order', 'created_at')

    # Attach teacher names
    teachers = Employee.objects.filter(role="teacher")
    teacher_map = {str(t.emp_uuid): t for t in teachers}

    for course in courses:
        teacher_names = []
        if course.teacher_ids:
            for uuid_str in course.teacher_ids:
                teacher = teacher_map.get(uuid_str)
                if teacher:
                    teacher_names.append(f"{teacher.name} ({teacher.emp_id})")
        course.teacher_names = teacher_names

    return render(request, "courses.html", {
        "courses": courses
    })
