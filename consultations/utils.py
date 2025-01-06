from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_booking_confirmation(booking):
    subject = 'Consultation Booking Confirmation'
    context = {
        'user': booking.user,
        'booking': booking,
        'package': booking.package
    }
    
    html_message = render_to_string('consultation/emails/booking_confirmation.html', context)
    plain_message = render_to_string('consultation/emails/booking_confirmation.txt', context)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.user.email],
        html_message=html_message
    )
