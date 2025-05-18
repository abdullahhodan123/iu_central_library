

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Transactions, Account
from .forms import DepositeForm
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string

class DepositMoneyView(CreateView):
    form_class = DepositeForm
    template_name = 'deposite.html'
    success_url = reverse_lazy('deposit_money')  # Update this as needed

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        try:
            account = Account.objects.get(user=self.request.user)
        except Account.DoesNotExist:
            account = Account.objects.create(user=self.request.user)
        
        # Update the account balance
        account.balance += amount
        account.save(update_fields=['balance'])

        # Create and save the Transaction record
        transaction = form.save(commit=False)
        transaction.account = account
        # Set other fields if necessary
        # transaction.balance = account.balance  # if required
        transaction.save()

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))} TK was deposited to your account successfully'
        )
        mail_subject="Deposite message"
        message=render_to_string('deposite_mail.html',{
            'user':self.request.user,
            'amount':amount,
            

        })
        to_email=self.request.user.email
        send_email=EmailMultiAlternatives(mail_subject,'',to=[to_email])
        send_email.attach_alternative(message,"text/html")
        send_email.send()

        return super().form_valid(form)
