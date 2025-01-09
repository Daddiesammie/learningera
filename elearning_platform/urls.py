from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import HomeView
urlpatterns = [
    path('admin/', include("django_admin_kubi.urls")),
    path('users/', include('users.urls')),
    path('', HomeView.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('terms/', TemplateView.as_view(template_name='legal/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='legal/privacy.html'), name='privacy'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('consultations/', include('consultations.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('payments/', include('payments.urls')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('testimonials/', include('testimonials.urls', namespace='testimonials')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)