from django.contrib import admin
from .models import ConsultationPackage, ConsultationBooking

@admin.register(ConsultationPackage)
class ConsultationPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(ConsultationBooking)
class ConsultationBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'booking_date', 'booking_time', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('payment_id', 'created_at')
