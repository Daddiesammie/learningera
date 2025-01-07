from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initialize/<str:payment_type>/<int:item_id>/', views.initialize_payment, name='initialize_payment'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('admin/verify-payment/<int:payment_id>/', views.admin_verify_payment, name='admin_verify_payment'),
    path('admin/cancel-payment/<int:payment_id>/', views.admin_cancel_payment, name='admin_cancel_payment'),
]
