from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Artisan

# نموذج تقييم المستخدم
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment.strip():
            raise forms.ValidationError("Comment cannot be empty")
        return comment

# نموذج تسجيل مستخدم حقيقي
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# نموذج تسجيل الحرفي
class ArtisanRegisterForm(forms.ModelForm):
    class Meta:
        model = Artisan
        fields = ['name', 'email', 'phone', 'service', 'city', 'experience', 'description', 'image']
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'service': 'Your Service',
            'city': 'City',
            'experience': 'Years of Experience',
            'description': 'Describe your experience',
            'image': 'Profile Picture',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'service': forms.TextInput(attrs={'placeholder': 'Enter your service'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Enter years of experience'}),
            'description': forms.Textarea(attrs={'placeholder': 'Briefly describe your experience', 'rows': 4}),
        }