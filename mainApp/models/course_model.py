from django.db import models
from datetime import datetime

from utils.send_course_email import send_new_course_email



# class Course(models.Model):
#     course_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

#     teacher_ids = models.JSONField(blank=True, null=True)  # e.g. ["uuid1", "uuid2"]

#     title = models.CharField(max_length=200)
#     subtitle = models.CharField(max_length=300, blank=True)
#     description = models.TextField(blank=True)

#     price = models.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         default=0.00,
#         help_text="Course fee in INR (e.g. 4999.00)"
#     )
#     discounted_price = models.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         null=True, 
#         blank=True,
#         help_text="Discounted price if there's an offer (leave blank if same as price)"
#     )
    
#     duration_display = models.CharField(
#         max_length=50,
#         blank=True,
#         default='',
#         help_text="Display text for course duration, e.g. '4m - 6m', '3 Months Live'"
#     )

#     is_new = models.BooleanField(default=False)
#     email_sent = models.BooleanField(default=False)

#     features = models.JSONField(default=list)  # e.g. ["3 Months Live", "5+ Projects", ...]

#     order = models.PositiveIntegerField(default=0)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['order', 'created_at']
#         verbose_name = "Course"
#         verbose_name_plural = "Courses"

#     def save(self, *args, **kwargs):
#         creating = self.pk is None  

#         # Auto-generate course_id (only on creation)
#         if creating and not self.course_id:
#             year = datetime.now().year
#             last_course = Course.objects.filter(
#                 course_id__startswith=f"C-{year}"
#             ).order_by('-created_at').first()  

#             if last_course and last_course.course_id:
#                 try:
#                     last_number = int(last_course.course_id.split('-')[-1])
#                     new_number = last_number + 1
#                 except (ValueError, IndexError):
#                     new_number = 1
#             else:
#                 new_number = 1

#             self.course_id = f"C-{year}-{new_number:04d}"  # 0001, 0002... better readability

#         # Save the main object first
#         super().save(*args, **kwargs)

#         # Send email only on creation and if not already sent
#         if creating and not self.email_sent:
#             try:
#                 send_new_course_email(self)  # your email function
#                 self.email_sent = True
#                 super().save(update_fields=['email_sent'])  # efficient
#             except Exception as e:
#                 print(f"Email sending failed for {self.title}: {e}")
#                 # Optional: logger.error(...) in production

#     def __str__(self):
#         return f"{self.course_id or 'New'} - {self.title}"

#     # Optional: nice helper methods
#     @property
#     def display_price(self):
#         """For templates: show discounted if available"""
#         if self.discounted_price is not None and self.discounted_price < self.price:
#             return self.discounted_price
#         return self.price

#     @property
#     def has_discount(self):
#         return self.discounted_price is not None and self.discounted_price < self.price


# class Course(models.Model):
#     course_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

#     teacher_ids = models.JSONField(blank=True, null=True)

#     title = models.CharField(max_length=200)
#     subtitle = models.CharField(max_length=300, blank=True)
#     description = models.TextField(blank=True)

#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0.00,
#         help_text="Course fee in INR (e.g. 4999.00)"
#     )

#     discounted_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         help_text="Discounted price if there's an offer"
#     )

#     duration_display = models.CharField(
#         max_length=50,
#         blank=True,
#         default='',
#         help_text="Display text for course duration"
#     )

#     is_new = models.BooleanField(default=False)
#     email_sent = models.BooleanField(default=False)

#     features = models.JSONField(default=list)

#     order = models.PositiveIntegerField(default=0)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['order', 'created_at']

#     def __str__(self):
#         return f"{self.course_id or 'New'} - {self.title}"


#     # ✅ DISPLAY PRICE
#     @property
#     def display_price(self):
#         if self.discounted_price and self.discounted_price < self.price:
#             return self.discounted_price
#         return self.price


#     # ✅ CHECK IF DISCOUNT EXISTS
#     @property
#     def has_discount(self):
#         return self.discounted_price is not None and self.discounted_price < self.price


#     # ✅ CALCULATE DISCOUNT %
#     @property
#     def discount_percentage(self):
#         if self.discounted_price and self.price and self.discounted_price < self.price:
#             discount = ((self.price - self.discounted_price) / self.price) * 100
#             return round(discount)
#         return 0

from django.db import models
from datetime import datetime
from utils.send_course_email import send_new_course_email


class Course(models.Model):
    course_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    teacher_ids = models.JSONField(blank=True, null=True)

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Course fee in INR (e.g. 4999.00)"
    )

    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Discounted price if there's an offer"
    )

    duration_display = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Display text for course duration"
    )

    is_new = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    features = models.JSONField(default=list)

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.course_id or 'New'} - {self.title}"


    # ✅ AUTO COURSE ID + EMAIL LOGIC
    def save(self, *args, **kwargs):
        creating = self.pk is None

        # Auto Generate Course ID
        if creating and not self.course_id:
            year = datetime.now().year

            last_course = Course.objects.filter(
                course_id__startswith=f"C-{year}"
            ).order_by('-created_at').first()

            if last_course and last_course.course_id:
                try:
                    last_number = int(last_course.course_id.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1

            self.course_id = f"C-{year}-{new_number:04d}"

        # Save first
        super().save(*args, **kwargs)

        # Send email only when checkbox is checked while creating course
        if creating and self.email_sent:
            try:
                send_new_course_email(self)
            except Exception as e:
                print(f"Email sending failed: {e}")


    # ✅ DISPLAY PRICE
    @property
    def display_price(self):
        if self.discounted_price and self.discounted_price < self.price:
            return self.discounted_price
        return self.price


    # ✅ CHECK IF DISCOUNT EXISTS
    @property
    def has_discount(self):
        return self.discounted_price is not None and self.discounted_price < self.price


    # ✅ CALCULATE DISCOUNT %
    @property
    def discount_percentage(self):
        if self.discounted_price and self.price and self.discounted_price < self.price:
            discount = ((self.price - self.discounted_price) / self.price) * 100
            return round(discount)
        return 0
