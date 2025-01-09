from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('rate/', views.rate_course, name='rate_course'),  # Moved before slug pattern
    path('my-courses/', views.my_courses, name='my_courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]
