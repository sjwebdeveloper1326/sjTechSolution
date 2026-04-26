from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from mainApp.forms import TestimonialForm
from mainApp.models import Testimonial


# READ (List)
def testimonial_list(request):
    if not request.user.is_authenticated:
        raise Http404()

    testimonial_list = Testimonial.objects.all().order_by('-id')

    paginator = Paginator(testimonial_list, 5)
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)

    return render(request, 'testimonialCRUD/testimonial_list.html', {
        'testimonials': testimonials
    })


# CREATE
# def add_testimonial(request):
#     # if not request.user.is_authenticated:
#     #     raise Http404()

#     if request.method == "POST":
#         form = TestimonialForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Testimonial added successfully! ✔")
#             return redirect('testimonial_list')
#         else:
#             messages.error(request, "Please fix the errors ❌")
#     else:
#         form = TestimonialForm()

#     return render(request, 'testimonialCRUD/testimonial_form.html', {'form': form})

def add_testimonial(request):

    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully! ✔")

            # 🔥 CONDITION BASED REDIRECT
            if request.user.is_authenticated:
                return redirect('testimonial_list')   
            else:
                return redirect('testimonial')        

        else:
            messages.error(request, "Please fix the errors ❌")
    else:
        form = TestimonialForm()

    return render(request, 'testimonialCRUD/testimonial_form.html', {'form': form})

# UPDATE
def edit_testimonial(request, id):
    if not request.user.is_authenticated:
        raise Http404()

    testimonial = get_object_or_404(Testimonial, id=id)

    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully! ✔")
            return redirect('testimonial_list')
        else:
            messages.error(request, "Please fix the errors ❌")
    else:
        form = TestimonialForm(instance=testimonial)

    return render(request, 'testimonialCRUD/testimonial_form.html', {'form': form})


# DELETE
def delete_testimonial(request, id):
    if not request.user.is_authenticated:
        raise Http404()

    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.delete()
    messages.success(request, "Testimonial deleted successfully! 🗑️")
    return redirect('testimonial_list')