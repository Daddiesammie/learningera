from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('book/<int:package_id>/', views.book_consultation, name='book_consultation'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
