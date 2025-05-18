from django.db import models

from catagory.models import Catagory
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    book_name=models.CharField(max_length=100)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    author=models.CharField(max_length=100,default='author_name')
    description=models.TextField()
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='book/media/uploads/', null=True, blank=True)
    quantity=models.IntegerField(default=0)

    def __str__(self):
        return self. book_name

class Comment(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=30)
    email=models.EmailField()
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return  f"Comments By {self.name}"


