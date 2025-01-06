from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import initialize_payment
from courses.models import Course, Enrollment
from consultations.models import ConsultationBooking

@login_required
def process_course_payment(request, course_id):
    if request.method != 'POST':
        messages.error(request, 'Invalid request method')
        return redirect('courses:course_detail', slug=course.slug)
        
    course = Course.objects.get(id=course_id)
    print(f"Processing payment for course: {course.title}")  # Debug line
    
    try:
        response = initialize_payment(
            request=request,
            amount=float(course.price),
            email=request.user.email,
            payment_type='course',
            item_id=course_id
        )
        print(f"Payment response: {response}")  # Debug line
        
        if response['status'] == 'success':
            return redirect(response['data']['link'])
        else:
            messages.error(request, f"Payment initialization failed: {response.get('message', '')}")
            return redirect('courses:course_detail', slug=course.slug)
            
    except Exception as e:
        print(f"Payment error: {str(e)}")  # Debug line
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('courses:course_detail', slug=course.slug)


@login_required
def process_consultation_payment(request, booking_id):
    booking = ConsultationBooking.objects.get(id=booking_id)
    
    try:
        response = initialize_payment(
            request=request,
            amount=float(booking.consultation_type.price),
            email=request.user.email,
            payment_type='consultation',
            item_id=booking_id
        )
        
        if response['status'] == 'success':
            return redirect(response['data']['link'])
        else:
            messages.error(request, 'Payment initialization failed')
            return redirect('consultation:booking_detail', pk=booking_id)
            
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('consultation:booking_detail', pk=booking_id)

@login_required
def verify_payment(request):
    tx_ref = request.GET.get('tx_ref', '')
    status = request.GET.get('status', '')
    
    if status == 'successful':
        # Extract payment type and item ID from tx_ref
        payment_type, item_id, _ = tx_ref.split('_')
        
        if payment_type == 'course':
            # Handle course enrollment
            Enrollment.objects.create(
                user=request.user,
                course_id=item_id,
                paid=True
            )
            messages.success(request, 'Course enrollment successful!')
            return redirect('courses:my_courses')
            
        elif payment_type == 'consultation':
            # Handle consultation booking
            booking = ConsultationBooking.objects.get(id=item_id)
            booking.payment_status = 'paid'
            booking.save()
            messages.success(request, 'Consultation booking confirmed!')
            return redirect('consultation:booking_detail', pk=item_id)
    
    messages.error(request, 'Payment verification failed')
    return redirect('dashboard')
