from django.db import models
from django.contrib.auth.models import User

from book.models import Book





class BorrowBooks(models.Model):
    user=models.ForeignKey(User,related_name='Borrow',on_delete=models.CASCADE)
    
    
    book=models.ForeignKey(Book,related_name='Borrow',on_delete=models.CASCADE)
    borrow_date=models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False) 
    is_returned = models.BooleanField(default=False)



    def __str__(self):
        user_name = self.user.first_name if self.user.first_name else self.user.username
        return f"{user_name} borrowed {self.book.book_name}"
    


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    roll = models.IntegerField( null=True, blank=True,default='0000000',unique=True)
    reg = models.IntegerField( null=True, blank=True,default='0000',unique=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    session = models.CharField(max_length=20, null=True, blank=True,default='2020-2021')

    def __str__(self):
        return self.user.username
    
    






