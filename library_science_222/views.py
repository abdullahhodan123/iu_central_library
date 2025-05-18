from django.shortcuts import render
from book.models import  Book
from catagory.models import Catagory
from django.core.paginator import Paginator


def home(request,catagory_slug=None):
    data=Book.objects.all()
    query=request.GET.get('query')

    if catagory_slug is not None:
      catagory=Catagory.objects.get(slug=catagory_slug)
      data=Book.objects.filter(catagory=catagory)

    if query:
      data=Book.objects.filter(book_name__icontains=query)  

    paginator = Paginator(data,8)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  

    all_catagory=Catagory.objects.all()
   
    return render(request,'home.html',{'data':page_obj,'catagory':all_catagory,'query':query})


def about_library(request):
   return render(request,'about_library.html')


def gellary(request):
   return render(request,'gellary.html')