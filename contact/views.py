from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save to database
            
            # Send email
            send_mail(
                f'Contact Form: {form.cleaned_data["subject"]}',
                f'From: {form.cleaned_data["name"]} ({form.cleaned_data["email"]})\n\n{form.cleaned_data["message"]}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact:contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})
