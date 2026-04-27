from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Artisan, ServiceRequest, Service, Complaint
from django.contrib.auth.forms import UserCreationForm


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
    


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ArtisanRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    services_count = forms.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        model = Artisan
        fields = [
            'name',
            'city',
            'phone',
            'email',
            'experience',
            'description',
            'image'
        ]

        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'city': 'City',
            'experience': 'Years of Experience',
            'description': 'Describe your experience',
            'image': 'Profile Picture',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Enter years of experience'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'Briefly describe your experience',
                'rows': 4
            }),
        }


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service', 'phone', 'message']

    def __init__(self, *args, **kwargs):
        artisan = kwargs.pop('artisan', None)
        super().__init__(*args, **kwargs)

        # 🔥 هذا هو التصليح الوحيد المهم
        if artisan:
            self.fields['service'].queryset = Service.objects.filter(artisan=artisan)
        else:
            self.fields['service'].queryset = Service.objects.all()

        # نفس الستايل تاعك بدون تغيير
        self.fields['service'].widget.attrs.update({
            'class': 'form-control'
        })
        
        
from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['service', 'reason', 'description', 'attachment']

        widgets = {
            'service': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'reason': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
        }