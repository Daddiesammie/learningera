from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
            'rating': forms.Select(attrs={
                'class': 'rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'
            })
        }
