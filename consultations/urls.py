from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('book/<int:package_id>/', views.book_consultation, name='book_consultation'),
    path('confirm-payment/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),
]
