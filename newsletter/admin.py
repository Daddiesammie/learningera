from django.contrib import admin
from django.core.mail import send_mass_mail
from django.contrib import messages
from django.utils import timezone
from .models import Subscriber, Newsletter

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_at'
    actions = ['activate_subscribers', 'deactivate_subscribers']

    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscribers have been activated.')
    activate_subscribers.short_description = 'Activate selected subscribers'

    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscribers have been deactivated.')
    deactivate_subscribers.short_description = 'Deactivate selected subscribers'

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent_at', 'is_sent')
    list_filter = ('is_sent',)
    search_fields = ('subject', 'content')
    date_hierarchy = 'created_at'
    actions = ['send_newsletter']
    readonly_fields = ('sent_at', 'is_sent')
    
    # Add these new configurations
    list_per_page = 20
    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'send_newsletter' in actions:
            actions['send_newsletter'][0].short_description = '📧 Send selected newsletters to subscribers'
        return actions


    def send_newsletter(self, request, queryset):
        for newsletter in queryset:
            if newsletter.is_sent:
                self.message_user(
                    request,
                    f'Newsletter "{newsletter.subject}" has already been sent.',
                    messages.WARNING
                )
                continue

            subscribers = Subscriber.objects.filter(is_active=True)
            if not subscribers.exists():
                self.message_user(
                    request,
                    'No active subscribers found.',
                    messages.WARNING
                )
                continue

            emails = [
                (
                    newsletter.subject,
                    newsletter.content,
                    'your-from-email@example.com',
                    [subscriber.email]
                )
                for subscriber in subscribers
            ]

            try:
                send_mass_mail(emails, fail_silently=False)
                newsletter.is_sent = True
                newsletter.sent_at = timezone.now()
                newsletter.save()
                self.message_user(
                    request,
                    f'Newsletter "{newsletter.subject}" sent successfully to {len(subscribers)} subscribers.',
                    messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request,
                    f'Error sending newsletter "{newsletter.subject}": {str(e)}',
                    messages.ERROR
                )

    send_newsletter.short_description = 'Send selected newsletters'
