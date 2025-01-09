# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from .forms import UserRegistrationForm, UserProfileForm, CustomPasswordResetForm
from .models import CustomUser
from consultations.models import ConsultationBooking
from payments.models import Payment
from courses.models import Enrollment

def register(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome aboard!')
            return redirect('users:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required(login_url='users:login')
def dashboard(request):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=180)
    
    # Get successful payments
    successful_payments = Payment.objects.filter(
        user=request.user,
        status='success'
    ).select_related('course')
    
    # Payment History
    payment_history = Payment.objects.filter(
        user=request.user
    ).select_related('course').order_by('-created_at')[:5]
    
    # Monthly course purchases
    monthly_data = []
    for i in range(6):
        month_start = (end_date - timedelta(days=30 * i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        count = Payment.objects.filter(
            user=request.user,
            status='success',
            course__isnull=False,  # Only count course purchases
            created_at__range=(month_start, month_end)
        ).count()
        
        monthly_data.append({
            'month': month_start.strftime('%b'),
            'count': count
        })
    
    monthly_data.reverse()
    total_consultations = ConsultationBooking.objects.filter(
        user=request.user,
        status='confirmed'  # or include other statuses if needed
    ).count()
    
    context = {
        'successful_payments': successful_payments,
        'payment_history': payment_history,
        'total_spent': successful_payments.aggregate(total=Sum('amount'))['total'] or 0,
        'total_consultations': total_consultations,
        'upcoming_consultations': ConsultationBooking.objects.filter(
            user=request.user,
            status='confirmed',
            booking_date__gte=timezone.now().date()
        ).order_by('booking_date', 'booking_time'),
        'monthly_data': monthly_data,
        'recent_courses': Enrollment.objects.filter(
            user=request.user
        ).select_related('course').order_by('-date_enrolled')[:5]
    }
    return render(request, 'users/dashboard.html', context)



@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'users/profile.html', context)

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

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/emails/password_reset_email.html'
    subject_template_name = 'users/emails/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')