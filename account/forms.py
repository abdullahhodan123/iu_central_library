from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import BorrowBooks,Account
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



class UserRegistrationForm(UserCreationForm):
    # first_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    # last_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    # email=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))

    
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    roll=forms.IntegerField(required=True)
    department=forms.CharField(required=True)
    reg=forms.IntegerField(required=True)
    session=forms.CharField(required=True)
    email=forms.CharField(required=True)
    
    

    class Meta:
        model = User
        fields=['username','first_name','last_name','email','roll','reg','department','session','password1','password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        roll = cleaned_data.get('roll')
        reg = cleaned_data.get('reg')

        if Account.objects.filter(roll=roll).exists():
            self.add_error('roll', "This roll number is already registered.")
        if Account.objects.filter(reg=reg).exists():
            self.add_error('reg', "This registration number is already registered.")


class UserUpdateForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']   

