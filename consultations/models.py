from django.db import models
from django.contrib.auth import get_user_model

class ConsultationPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class ConsultationBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    package = models.ForeignKey(ConsultationPackage, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-booking_date', '-booking_time']

    def __str__(self):
        return f"Consultation with {self.user.username} on {self.booking_date}"
