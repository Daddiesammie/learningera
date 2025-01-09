from newsletter.forms import SubscribeForm

def newsletter_form(request):
    return {
        'subscribe_form': SubscribeForm()
    }
