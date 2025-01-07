from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from django.http import JsonResponse
from .models import ConsultationPackage, ConsultationBooking

class PackageListView(ListView):
    model = ConsultationPackage
    template_name = 'consultation/package_list.html'
    context_object_name = 'packages'
    queryset = ConsultationPackage.objects.filter(is_active=True)

from django.http import JsonResponse

@login_required
def book_consultation(request, package_id):
    if request.method == 'POST':
        package = get_object_or_404(ConsultationPackage, id=package_id)
        
        booking = ConsultationBooking.objects.create(
            user=request.user,
            package=package,
            booking_date=request.POST.get('date'),
            booking_time=request.POST.get('time'),
            status='pending'
        )
        
        return JsonResponse({
            'booking_id': booking.id,
            'success': True
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def my_bookings(request):
    bookings = ConsultationBooking.objects.filter(user=request.user).order_by('-booking_date')
    context = {
        'bookings': bookings,
        'pending_bookings': bookings.filter(status='pending'),
        'confirmed_bookings': bookings.filter(status='confirmed'),
        'completed_bookings': bookings.filter(status='completed')
    }
    return render(request, 'consultation/my_bookings.html', context)

@login_required
def booking_detail(request, pk):
    booking = ConsultationBooking.objects.get(id=pk)
    return render(request, 'consultation/booking_detail.html', {'booking': booking})