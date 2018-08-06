from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User_Table
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'input100', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}))

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='',
                               widget=forms.TextInput(attrs={'class': 'usernamefield',
                                                             'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=30, required=False, label='',
                                 widget=forms.TextInput(attrs={'class': 'firstnamefield',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=False, label='',
                                widget=forms.TextInput(attrs={'class': 'lastnamefield',
                                                              'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=254, label=''
                             , widget=forms.TextInput(attrs={'class': 'emailfield',
                                                             'placeholder': 'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'passwordfield',
                                                                            'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'passwordfield',
                                                                            'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UserProfileForm(forms.ModelForm):
    User_Favorite_Brewery_Type = forms.CharField(max_length=30, label='',
                                                 widget=forms.TextInput(attrs={'class': 'breweryfield',
                                                                               'placeholder': 'Favourite Brewery'}))
    User_Max_Distance = forms.CharField(max_length=30, label='',
                                        widget=forms.TextInput(attrs={'class': 'distancefield',
                                                                      'placeholder': 'Max Distance'}))
    User_Beer_Stout = forms.BooleanField(label='Stout',
                                         widget=forms.CheckboxInput(attrs={'class': 'beerfield'}))
    User_Beer_Lager = forms.BooleanField(label='Lager',
                                         widget=forms.CheckboxInput(attrs={'class': 'beerfield'}))
    User_Beer_IPA = forms.BooleanField(label='IPA',
                                       widget=forms.CheckboxInput(attrs={'class': 'beerfield'}))
    User_Beer_Cider = forms.BooleanField(label='Cider',
                                         widget=forms.CheckboxInput(attrs={'class': 'beerfield'}))
    User_Beer_Pilsner = forms.BooleanField(label='Pilsner',
                                           widget=forms.CheckboxInput(attrs={'class': 'beerfield'}))
    User_Beer_Ale = forms.BooleanField(label='Ale',
                                       widget=forms.CheckboxInput(attrs={'class': 'beerfield'}))
    User_Beer_Weiss = forms.BooleanField(label='Weiss',
                                         widget=forms.CheckboxInput(attrs={'class': 'beerfield'}))
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