from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from .models import ConsultationPackage, ConsultationBooking
import requests

class PackageListView(ListView):
    model = ConsultationPackage
    template_name = 'consultation/package_list.html'
    context_object_name = 'packages'
    queryset = ConsultationPackage.objects.filter(is_active=True)

@login_required
def book_consultation(request, package_id):
    package = ConsultationPackage.objects.get(id=package_id)
    
    if request.method == 'POST':
        booking = ConsultationBooking.objects.create(
            user=request.user,
            package=package,
            booking_date=request.POST['date'],
            booking_time=request.POST['time']
        )

        headers = {
            'Authorization': f'Bearer {settings.FLW_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'tx_ref': f'consultation-{booking.id}',
            'amount': str(package.price),
            'currency': 'NGN',
            'redirect_url': request.build_absolute_uri(
                reverse('consultations:payment_callback')
            ),
            'customer': {
                'email': request.user.email,
                'name': f'{request.user.first_name} {request.user.last_name}'
            },
            'meta': {
                'booking_id': booking.id
            }
        }

        response = requests.post(
            'https://api.flutterwave.com/v3/payments',
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            return JsonResponse({
                'payment_url': response.json()['data']['link']
            })
        
        return JsonResponse({'error': 'Payment initialization failed'}, status=400)

    return render(request, 'consultation/booking_form.html', {'package': package})

@login_required
def confirm_payment(request, booking_id):
    booking = ConsultationBooking.objects.get(id=booking_id)
    booking.status = 'confirmed'
    booking.save()
    
    return JsonResponse({'success': True})
