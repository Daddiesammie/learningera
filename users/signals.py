from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        context = {
            'username': instance.username,
            'login_url': f"{settings.SITE_URL}/login"
        }
        
        html_message = render_to_string('users/emails/welcome.html', context)
        plain_message = render_to_string('users/emails/welcome.txt', context)
        
        send_mail(
            subject='Welcome to Our Platform!',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=html_message
        )
