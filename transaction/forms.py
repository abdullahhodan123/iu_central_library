# from django import forms 
# from .models import Transactions, Account
# from django.contrib.auth.models import User

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transactions
#         fields = ['amount']

#     def __init__(self, *args, **kwargs):
#         self.account = kwargs.pop('account', None)
#         super().__init__(*args, **kwargs)

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.account = self.account
        
#         if commit:
#             instance.save()
#         return instance

# class DepositeForm(TransactionForm):
#     def clean_amount(self):
#         min_deposit_amount = 100
#         amount = self.cleaned_data.get('amount')

#         if amount < min_deposit_amount:
#             raise forms.ValidationError(
#                 f'You need to deposit a minimum of {min_deposit_amount} TK'
#             )
#         return amount

# forms.py
from django import forms
from .models import Transactions

class DepositeForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount']

    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')

        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit a minimum of {min_deposit_amount} TK'
            )
        return amount

    def save(self, commit=True):
        # Do not set the account here; it should be set in the view
        transaction = super().save(commit=False)
        if commit:
            transaction.save()
        return transaction
