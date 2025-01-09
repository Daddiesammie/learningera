from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            })
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email.lower()  # Normalize email addresses to lowercase

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'profile_image', 'bio', 'phone_number', 'website', 'location', 'social_links']
        widgets = {
            'profile_image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'phone_number': forms.TextInput(),
            'website': forms.URLInput(),
            'location': forms.TextInput(),
            'social_links': forms.Textarea(attrs={'rows': 4}),
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('There is no user registered with this email address.')
        return email
