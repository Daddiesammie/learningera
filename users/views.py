from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from courses.models import Enrollment

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome aboard!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(
        user=request.user,
        paid=True
    ).select_related('course')
    
    context = {
        'enrollments': enrollments,
        'active_courses': enrollments.filter(status='active'),
        'completed_courses': enrollments.filter(status='completed')
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def public_profile(request, slug):
    user = get_object_or_404(CustomUser, slug=slug)
    context = {
        'profile_user': user,
        'completed_courses': Enrollment.objects.filter(
            user=user,
            status='completed'
        ).select_related('course')
    }
    return render(request, 'users/public_profile.html', context)
