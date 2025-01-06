from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    social_links = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'bio', 'phone_number', 'website', 'location', 'social_links']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
