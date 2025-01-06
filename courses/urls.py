from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('rate/', views.rate_course, name='rate_course'),
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]
