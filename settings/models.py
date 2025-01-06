from django.db import models
from django.core.cache import cache

class SiteSettings(models.Model):
    # Basic Site Info
    site_name = models.CharField(max_length=100, default="LearnHub")
    site_logo = models.ImageField(upload_to='site/logo/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site/favicon/', null=True, blank=True)
    
    # Contact Information
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Hero Section
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='site/hero/', null=True, blank=True)
    
    # Social Links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    
    # SEO Fields
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    
    # Additional Settings
    maintenance_mode = models.BooleanField(default=False)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache when settings are updated
        cache.delete('site_settings')

    @classmethod
    def get_settings(cls):
        # Get cached settings or create new cache
        settings = cache.get('site_settings')
        if not settings:
            settings = cls.objects.first()
            if not settings:
                settings = cls.objects.create()
            cache.set('site_settings', settings)
        return settings
