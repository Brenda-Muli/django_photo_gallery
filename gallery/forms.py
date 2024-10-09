from .models import Gallery
from django import forms
from django.forms.widgets  import PasswordInput, TextInput
from  django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class PictureForm(forms.ModelForm):
  class Meta:
    model = Gallery
    fields = ['title', 'image', 'description', 'tag_category']
    widgets = {
       'title': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Enter a Title for your picture!'}),
       'description':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a Description for your picture!'}),
       'tag_category': forms.Select(choices=Gallery.TAG_CHOICES)
    }


class DisplayForm(forms.ModelForm):
  class Meta:
    model = Gallery
    fields = ['title', 'description', 'tag_category', 'likes']
    