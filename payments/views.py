from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from .models import Payment
from .utils import PaystackPayment, generate_payment_reference
from courses.models import Course, Enrollment
from consultations.models import ConsultationBooking
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse


@staff_member_required
def admin_verify_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    paystack = PaystackPayment()
    response = paystack.verify_payment(payment.reference)

    if response['status'] and response['data']['status'] == 'success':
        payment.status = 'success'
        payment.save()
        messages.success(request, 'Payment verified successfully')
    else:
        messages.error(request, 'Payment verification failed')

    return redirect('admin:payments_payment_changelist')

@staff_member_required
def admin_cancel_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = 'cancelled'
    payment.save()
    messages.success(request, 'Payment cancelled successfully')
    return redirect('admin:payments_payment_changelist')


@login_required
def initialize_payment(request, payment_type, item_id):
    try:
        if payment_type == 'course':
            item = Course.objects.get(id=item_id)
            amount = float(item.price)
        else:
            item = ConsultationBooking.objects.get(id=item_id)
            amount = float(item.package.price)

        reference = generate_payment_reference()
        
        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            payment_type=payment_type,
            amount=amount,
            reference=reference,
            course=item if payment_type == 'course' else None,
            consultation=item if payment_type == 'consultation' else None
        )

        # Initialize Paystack payment
        paystack = PaystackPayment()
        response = paystack.initialize_payment(
            request.user.email,
            amount,
            reference
        )

        if response['status']:
            return JsonResponse({
                'status': 'success',
                'authorization_url': response['data']['authorization_url']
            })
        return JsonResponse({'status': 'failed', 'message': response['message']})

    except Exception as e:
        return JsonResponse({'status': 'failed', 'message': str(e)})

@login_required
def verify_payment(request):
    reference = request.GET.get('reference')
    if not reference:
        return redirect('payment_failed')

    try:
        payment = Payment.objects.get(reference=reference)
        paystack = PaystackPayment()
        response = paystack.verify_payment(reference)

        if response['status'] and response['data']['status'] == 'success':
            # Update payment status
            payment.status = 'success'
            payment.save()

            # Process the successful payment
            if payment.payment_type == 'course':
                Enrollment.objects.create(
                    user=payment.user,
                    course=payment.course,
                    paid=True
                )
                return redirect('courses:my_courses')
            else:
                payment.consultation.status = 'confirmed'
                payment.consultation.save()
                return redirect('consultations:booking_detail', pk=payment.consultation.id)

        payment.status = 'failed'
        payment.save()
        return redirect('payment_failed')

    except Payment.DoesNotExist:
        return redirect('payment_failed')
    
@login_required
def payment_failed(request):
    context = {
        'title': 'Payment Failed',
        'support_email': 'support@saleselite.com',
        'support_phone': '+234 800 123 4567'
    }
    return render(request, 'payments/payment_failed.html', context)