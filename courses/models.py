from django.db import models
from django.urls import reverse
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_image = models.ImageField(upload_to='courses/images/', null=True)
    is_published = models.BooleanField(default=False)
    duration = models.CharField(max_length=50, default='8 weeks')
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')
    video_url = models.URLField(help_text="Enter the YouTube video URL", null=True)
    
    def get_youtube_id(self):
        """Extract YouTube video ID from URL"""
        if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
            if 'youtube.com' in self.video_url:
                return self.video_url.split('v=')[1].split('&')[0]
            else:
                return self.video_url.split('/')[-1]
        return None

    class Meta:
        ordering = ['-created_at']
    


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})
    
    @property
    def average_rating(self):
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        if avg is not None:
            return round(avg, 1)
        return 0


from django.contrib.auth import get_user_model

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('dropped', 'Dropped')
    )
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    paid = models.BooleanField(default=False)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_accessed = models.DateTimeField(auto_now=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [['user', 'course']]
        ordering = ['-last_accessed']

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

    def mark_as_completed(self):
        from django.utils import timezone
        self.status = 'completed'
        self.progress = 100
        self.completion_date = timezone.now()
        self.save()

    def update_progress(self, progress_value):
        self.progress = min(max(progress_value, 0), 100)
        if self.progress == 100:
            self.mark_as_completed()
        self.save()

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def days_enrolled(self):
        from django.utils import timezone
        return (timezone.now() - self.date_enrolled).days
    

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} rated {self.course.title}: {self.rating}"
