from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Testimonial
from .forms import TestimonialForm

def testimonial_list(request):
    testimonials = Testimonial.objects.filter(is_published=True)
    return render(request, 'testimonials/testimonial_list.html', {
        'testimonials': testimonials
    })

@login_required
def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Your testimonial has been submitted for review.')
            return redirect('home')
    else:
        form = TestimonialForm()
    
    return render(request, 'testimonials/submit_testimonial.html', {'form': form})
