from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Enrollment, CourseRating

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_image', 'price', 'level', 'duration', 'is_published', 'created_at', 'display_rating']
    list_filter = ['is_published', 'created_at', 'level']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['price', 'is_published', 'level', 'duration']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'slug', 'description', 'course_image', 'price', 'video_url')
        }),
        ('Settings', {
            'fields': ('is_published', 'level', 'duration')
        }),
    )

    def display_image(self, obj):
        if obj.course_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.course_image.url)
        return "No Image"
    display_image.short_description = 'Image'

    def display_rating(self, obj):
        rating = obj.average_rating
        return format_html('⭐ {}', rating)
    display_rating.short_description = 'Rating'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'progress_bar', 'paid', 'date_enrolled', 'last_accessed']
    list_filter = ['status', 'paid', 'date_enrolled']
    search_fields = ['user__username', 'user__email', 'course__title']
    date_hierarchy = 'date_enrolled'
    list_editable = ['status', 'paid']
    autocomplete_fields = ['user', 'course']
    list_per_page = 20
    
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('user', 'course', 'status', 'paid')
        }),
        ('Progress Information', {
            'fields': ('progress', 'completion_date')
        }),
    )

    def progress_bar(self, obj):
        return format_html(
            '<div style="width:100px; background-color: #f0f0f0; border-radius: 3px;">'
            '<div style="width: {}%; background-color: #4CAF50; height: 20px; border-radius: 3px;">'
            '<div style="padding: 0 5px; color: white;">{}</div>'
            '</div></div>',
            obj.progress,
            f"{obj.progress}%"
        )
    progress_bar.short_description = 'Progress'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user', 'course', 'date_enrolled', 'last_accessed']
        return []


@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'display_rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'course__title']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user', 'course']
    list_per_page = 20
    ordering = ['-created_at']

    def display_rating(self, obj):
        stars = '⭐' * obj.rating
        return format_html(stars)
    display_rating.short_description = 'Rating'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user', 'course', 'created_at']
        return []
