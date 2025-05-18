from django import forms 
from .models import Catagory

class CatagoryForm(forms.ModelForm):
    model=Catagory
    fields='__all__'
    


