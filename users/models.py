# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.username}-{str(uuid.uuid4())[:8]}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('users:public_profile', kwargs={'slug': self.slug})