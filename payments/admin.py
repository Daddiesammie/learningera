from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'amount', 'payment_type', 'status', 'created_at', 'payment_actions']
    list_filter = ['status', 'payment_type', 'created_at']
    search_fields = ['reference', 'user__email', 'user__username']
    readonly_fields = ['reference', 'paystack_payment_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('reference', 'user', 'amount', 'payment_type', 'status')
        }),
        ('Related Items', {
            'fields': ('course', 'consultation')
        }),
        ('Payment Details', {
            'fields': ('paystack_payment_id', 'created_at', 'updated_at')
        }),
    )

    def payment_actions(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">Verify</a>&nbsp;'
                '<a class="button" href="{}">Cancel</a>',
                reverse('payments:admin_verify_payment', args=[obj.id]),
                reverse('payments:admin_cancel_payment', args=[obj.id])
            )
        return obj.get_status_display()
    
    payment_actions.short_description = 'Actions'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'course', 'consultation')

    class Media:
        css = {
            'all': ('css/admin/payment.css',)
        }
        js = ('js/admin/payment.js',)
