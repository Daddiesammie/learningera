from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

def send_welcome_email(user):
    subject = 'Welcome to CourseArena!'
    context = {
        'user': user,
        'site_url': settings.SITE_URL + reverse('users:dashboard')
    }
    html_message = render_to_string('emails/welcome_email.html', context)
    
    send_mail(
        subject=subject,
        message='',
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )

def send_course_enrollment_email(user, course):
    subject = f'Enrolled: {course.title}'
    context = {
        'user': user,
        'course': course,
        'course_url': settings.SITE_URL + reverse('courses:course_detail', kwargs={'slug': course.slug})
    }
    html_message = render_to_string('emails/course_enrollment.html', context)
    
    send_mail(
        subject=subject,
        message='',
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )

def send_consultation_booking_email(booking):
    subject = 'Consultation Booking Confirmation'
    context = {
        'user': booking.user,
        'booking': booking,
        'booking_url': settings.SITE_URL + reverse('consultations:booking_detail', kwargs={'pk': booking.pk})
    }
    html_message = render_to_string('emails/consultation_booking.html', context)
    
    send_mail(
        subject=subject,
        message='',
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.user.email],
        fail_silently=False
    )
