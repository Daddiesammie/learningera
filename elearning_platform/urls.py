from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
urlpatterns = [
    path('users/', include('users.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('consultations/', include('consultations.urls')),
    path('payments/', include('payments.urls')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)