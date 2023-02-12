from django import forms
from .models import Photo, PhotoContext, Profile
from django.contrib.auth.models import User

# class PhotoContextForm(forms.ModelForm):
#     class Meta:
#         model = PhotoContext
#         fields = '__all__'

# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = Photo
#         fields = ['title', 'url']

class UpdateUserForm(forms.ModelForm):
    username = forms.Charfield(max_length=100, required=True)
    class Meta:
        model = User
        fields = ['username']

class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model= Profile
        fields = ['bio']