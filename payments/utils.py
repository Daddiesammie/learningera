import secrets
from django.conf import settings
import requests

class PaystackPayment:
    @staticmethod
    def initialize_payment(email, amount, reference):
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "amount": int(amount * 100),  # Convert to kobo
            "reference": reference,
            "callback_url": settings.PAYSTACK_CALLBACK_URL
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @staticmethod
    def verify_payment(reference):
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        response = requests.get(url, headers=headers)
        return response.json()

def generate_payment_reference():
    return f"PAY-{secrets.token_hex(8)}"
