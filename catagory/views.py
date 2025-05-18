from django.shortcuts import render,redirect
from . import forms


def catagory(request):
    if request.method=="POST":
        form=forms.CatagoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catagory')
        else:
            form=forms.CatagoryForm() 

    return render(request,'catagory.html',{form:'form'})



