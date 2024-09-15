from django import forms
from .models import Movie, User
from django.contrib.auth.forms import PasswordChangeForm

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'genre', 'releaseYear', 'rating', 'duration', 'description', 'production_company', 'country', 'language', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'releaseYear': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(10, 0, -1)], attrs={'class': 'form-rating'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'production_company': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }



class UserProfileForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ('username',)
        
class ChangePasswordForm(PasswordChangeForm):
    pass