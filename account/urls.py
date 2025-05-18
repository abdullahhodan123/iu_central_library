from django.contrib import admin
from django.urls import path
from .import views
from .views import ProfileView,Borrow


urlpatterns = [
   
    path('reg/',views.singup ,name='singup'),
   
    path('login/',views.UserLogInView.as_view(),name='user_login'),
  
    path('password/',views.Passwordchange,name='password'),
    
    path('logout/',views.logout,name='logout'),
    path('update/',views.UpdateData,name='update'),
    path('profile/', ProfileView.as_view(), name='profile'),  
    
    path('user/borrow/<int:book_id>/', views.Borrow, name='borrow_book'),
    path('account/user/return/<int:book_id>/', views.ReturnBook, name='return_book')

    

    
    
  
   
]
