from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import timedelta

from consultations.models import ConsultationBooking
from payments.models import Payment
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
    # Get the current date and 6 months ago date
    end_date = timezone.now()
    start_date = end_date - timedelta(days=180)
    
    successful_payments = Payment.objects.filter(
        user=request.user,
        status='success'
    ).select_related('course')
    
    # Get monthly consultation counts
    monthly_consultations = []
    current_date = start_date
    
    while current_date <= end_date:
        month_start = current_date.replace(day=1)
        if current_date.month == 12:
            month_end = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)
            
        count = ConsultationBooking.objects.filter(
            user=request.user,
            booking_date__range=(month_start, month_end)
        ).count()
        
        monthly_consultations.append(count)
        current_date = month_end + timedelta(days=1)

    # Base consultations queryset
    consultations = ConsultationBooking.objects.filter(user=request.user)
    
    # Upcoming consultations
    upcoming_consultations = consultations.filter(
        status='confirmed',
        booking_date__gte=timezone.now().date()
    ).order_by('booking_date', 'booking_time')

    context = {
        # Payment related context
        'successful_payments': successful_payments,
        'failed_payments': Payment.objects.filter(user=request.user, status='failed'),
        'total_spent': successful_payments.aggregate(total=Sum('amount'))['total'] or 0,
        'payment_history': Payment.objects.filter(user=request.user).select_related('course').order_by('-created_at'),
        
        # Consultation related context
        'upcoming_consultations': upcoming_consultations,
        'total_consultations': consultations.count(),
        'completed_consultations': consultations.filter(status='completed').count(),
        
        # Chart data
        'monthly_consultations': monthly_consultations,
        'consultation_months': [(end_date - timedelta(days=30*i)).strftime('%b') for i in range(5, -1, -1)],
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
