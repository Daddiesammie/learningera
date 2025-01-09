from django.shortcuts import redirect
from django.contrib import messages
from .forms import SubscribeForm

def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Welcome to our newsletter! You have successfully subscribed.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'This email is already subscribed to our newsletter.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))
