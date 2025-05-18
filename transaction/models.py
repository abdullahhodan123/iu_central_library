
from django.db import models
from django.contrib.auth.models import User
from account.models import Account


class Transactions(models.Model):
    account=models.ForeignKey(Account,related_name='transaction',on_delete=models.CASCADE)
    balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.00,null=True,blank=True)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    # amount_after_transaction=models.DecimalField(decimal_places=2,max_digits=12)

    def __str__(self):
        return self.account.username


