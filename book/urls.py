from django.contrib import admin
from django.urls import path
from . import views
from .views import DetailsBookView



urlpatterns = [
   
   path('hodan/',views. AddBook.as_view(),name='addbooks'),
   path('details/<int:id>',DetailsBookView.as_view(),name='details_book'),
]