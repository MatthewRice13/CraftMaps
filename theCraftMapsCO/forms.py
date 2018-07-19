from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User_Table

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_Table
        fields = ('User_Favorite_Brewery_Type',
                  'User_Max_Distance',
                  'User_Beer_Stout',
                  'User_Beer_Lager',
                  'User_Beer_IPA',
                  'User_Beer_Cider',
                  'User_Beer_Pilsner',
                  'User_Beer_Ale',
                  'User_Beer_Weiss',)