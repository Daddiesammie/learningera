# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

class UserProfileForm(forms.ModelForm):
    social_links = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter as JSON: {"twitter": "url", "linkedin": "url"}'}),
        required=False
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'profile_image', 'bio', 'phone_number', 'website', 'location', 'social_links']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_social_links(self):
        import json
        social_links = self.cleaned_data.get('social_links')
        if social_links:
            try:
                return json.loads(social_links)
            except json.JSONDecodeError:
                raise forms.ValidationError('Please enter valid JSON format')
        return {}

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('There is no user registered with this email address.')
        return email