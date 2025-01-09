from django.views.generic import TemplateView
from testimonials.models import Testimonial

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_published=True).order_by('-created_at')[:6]
        return context


