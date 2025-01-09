from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at', 'is_published']
    list_filter = ['is_published', 'rating']
    search_fields = ['user__username', 'content']
    actions = ['publish_testimonials', 'unpublish_testimonials']
    
    def publish_testimonials(self, request, queryset):
        queryset.update(is_published=True)
    
    def unpublish_testimonials(self, request, queryset):
        queryset.update(is_published=False)
