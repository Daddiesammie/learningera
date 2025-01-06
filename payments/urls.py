from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process-course/<int:course_id>/', views.process_course_payment, name='process_course_payment'),
    path('verify/', views.verify_payment, name='verify_payment'),
]
