from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from consultations.models import ConsultationBooking

class Payment(models.Model):
    PAYMENT_TYPES = (
        ('course', 'Course'),
        ('consultation', 'Consultation'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference = models.CharField(max_length=200, unique=True, null= True)
    paystack_payment_id = models.CharField(max_length=100, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    consultation = models.ForeignKey(ConsultationBooking, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.payment_type} payment - {self.reference}"

    def save_payment_info(self, paystack_response):
        self.paystack_payment_id = paystack_response.get('id')
        self.status = 'success' if paystack_response.get('status') == 'success' else 'failed'
        self.save()
