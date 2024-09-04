from django import forms
from .models import Movie, User
from django.contrib.auth.forms import PasswordChangeForm

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'genre', 'releaseYear']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'releaseYear': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ('username',)
        
class ChangePasswordForm(PasswordChangeForm):
    pass