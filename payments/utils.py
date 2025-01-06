import json
import requests
import time
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

def initialize_payment(request, amount, email, payment_type, item_id):
    current_site = get_current_site(request)
    tx_ref = f"{payment_type}_{item_id}_{int(time.time())}"
    
    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "tx_ref": tx_ref,
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": f"http://{current_site.domain}{reverse('payments:verify_payment')}",
        "payment_options": "card",
        "client": tx_ref,
        "customer": {
            "email": email,
            "name": request.user.get_full_name() or request.user.username,
            "phonenumber": "0903000000"
        },
        "customizations": {
            "title": "Course Payment",
            "description": "Payment for course enrollment",
            "logo": "https://example.com/logo.png"
        }
    }
    
    print(f"Using Secret Key: {settings.FLW_SECRET_KEY[:10]}...")  # Print first 10 chars of key
    print(f"Full Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        "https://api.flutterwave.com/v3/payments",
        headers=headers,
        json=payload
    )
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code in [200, 201]:
        response_data = response.json()
        return {
            'status': 'success',
            'data': {
                'link': response_data['data']['link']
            }
        }
    
    return {
        "status": "error",
        "message": "Payment initialization failed. Please check your payment details."
    }
