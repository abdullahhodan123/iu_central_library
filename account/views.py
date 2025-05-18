
# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from . import forms
from book.models import Book
from .models import BorrowBooks, Account
from django.views.generic import ListView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime,timedelta
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from django.contrib.staticfiles import finders 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.contrib.auth import login
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string


# def singup(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             messages.success(request, 'Account Created Successfully')
#             form.save()
#             return redirect('user_login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'sing_up.html', {'form': form, 'type': 'Singup'})

def singup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            roll = form.cleaned_data.get('roll')
            reg = form.cleaned_data.get('reg')
            department = form.cleaned_data.get('department')
            session = form.cleaned_data.get('session')

            # Update Account model (already created via signal)
            account = Account.objects.get(user=user)
            account.roll = roll
            account.reg = reg
            account.department = department
            account.session = session
            account.save()
            login(request, user)  # auto-login
            messages.success(request, 'Account Created and Logged in Successfully')
            return redirect('home')  # or redirect to 'profile'
    else:
        form = UserRegistrationForm()
    return render(request, 'sing_up.html', {'form': form, 'type': 'Signup'})




class UserLogInView(LoginView):
    template_name = 'sing_up.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'LogIn Successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'LogIn Unsuccessful')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


def Passwordchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password Updated Successfully")
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('user_login')


def UpdateData(request):
    if request.method == "POST":
        profile_form = forms.UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your Profile Data Is Updated Successfully!")
            return redirect("profile")
    else:
        profile_form = forms.UserUpdateForm(instance=request.user)
    return render(request, 'data_update.html', {'form': profile_form})


class ProfileView(ListView):
    model = BorrowBooks
    template_name = 'profile.html'
    context_object_name = 'Borrow'
    

    def get_queryset(self):
        return BorrowBooks.objects.filter(user=self.request.user).select_related('book')


# def Borrow(request, book_id):
#     book = get_object_or_404(Book, id=book_id)

#     if request.user.is_authenticated:
#         account = get_object_or_404(Account, user=request.user)

#         existing_borrow = BorrowBooks.objects.filter(user=request.user, book=book, is_returned=False).exists()
#         if existing_borrow:
#             messages.error(request, 'You have already borrowed this book')
#             return redirect('profile')

#         borrow = BorrowBooks.objects.create(user=request.user, book=book)
#         book.quantity -= 1
#         book.save()

#         # Generate professional PDF receipt
#         buffer = BytesIO()
#         p = canvas.Canvas(buffer, pagesize=A4)

#         width, height = A4
#         now = datetime.now().strftime("%d-%m-%y %H:%M:%S")
#         return_date = datetime.now() + timedelta(days=10)
#         formatted_return_date = return_date.strftime("%Y-%m-%d")

#         # Title
#         # p.setFillColor(colors.darkblue)
#         # p.setFont("Helvetica-Bold", 18)
#         # p.drawCentredString(width / 2, height - 100, "Library Book Borrow Receipt")
#         p.setFillColor(colors.green)
#         p.setFont("Helvetica-Bold", 20)
#         p.drawCentredString(width / 2, height - 60, "Central Library,IU")

#         p.setFont("Helvetica", 12)
#         p.drawCentredString(width / 2, height - 80, "Shantidanga, Kushtia-7003, Bangladesh")
#         p.setFont("Helvetica", 11)
#         p.drawCentredString(width / 2, height - 95, "Phone: +880-71-74902 | Email: info@iu.ac.bd")

#     # Horizontal line
#         p.setStrokeColor(colors.gray)
#         p.line(40, height - 105, width - 40, height - 105)

#     # Receipt Title
#         p.setFont("Helvetica-Bold", 16)
#         p.setFillColor(colors.black)
#         p.drawCentredString(width / 2, height - 130, "Library Book Borrow Receipt")
   

#         # Info block
#         p.setFillColor(colors.black)
#         p.setFont("Helvetica", 12)
#         p.drawString(100, height - 160, f"BorrowDate: {now}")
#         p.drawString(100, height - 180, f"Username: {request.user.username}")
#         p.drawString(100, height - 200, f"Full Name: {request.user.get_full_name() or 'N/A'}")
#         p.drawString(100, height - 220, f"Book Title: {book.book_name}")
#         p.drawString(100, height - 240, f"Author: {book.author}")
#         p.drawString(100, height - 260, f"Return Date:{formatted_return_date}")
       

#         # Footer
#         p.setFont("Helvetica-Oblique", 11)
#         p.setFillColor(colors.grey)
#         p.drawString(100, height - 300, "Thank you for using our library. Please return the book within the due date.")

#         # Finalize
#         p.showPage()
#         p.save()
#         buffer.seek(0)

#         # PDF response with download
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=borrow_receipt_{request.user.username}.pdf'
#         # return response
#         return redirect('profile')

#     else:
#         return redirect('login')


def Borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user.is_authenticated:
        account = get_object_or_404(Account, user=request.user)

        existing_borrow = BorrowBooks.objects.filter(user=request.user, book=book, is_returned=False).exists()
        if existing_borrow:
            messages.error(request, 'You have already borrowed this book')
            return redirect('profile')

        borrow = BorrowBooks.objects.create(user=request.user, book=book)
        book.quantity -= 1
        book.save()

        # Generate professional PDF receipt
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        now = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        return_date = datetime.now() + timedelta(days=10)
        formatted_return_date = return_date.strftime("%d-%m-%y")

        logo_path = finders.find('download.png')  # Make sure it's in your static folder
        if logo_path:
            p.drawImage(logo_path, 50, height - 110, width=40, height=70, preserveAspectRatio=True)

        

        # Title block
        p.setFillColor(colors.green)
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width / 2, height - 60, "Central Library, IU")

        p.setFont("Helvetica", 12)
        p.drawCentredString(width / 2, height - 80, "Shantidanga, Kushtia-7003, Bangladesh")
        p.setFont("Helvetica", 11)
        p.drawCentredString(width / 2, height - 95, "Phone: +880-71-74902 | Email: info@iu.ac.bd")

        # Horizontal line
        p.setStrokeColor(colors.gray)
        p.line(40, height - 105, width - 40, height - 105)

        # Receipt Title
        p.setFont("Helvetica-Bold", 16)
        p.setFillColor(colors.black)
        p.drawCentredString(width / 2, height - 130, "Library Book Borrow Receipt")

        # Prepare user & book info
       
        account = Account.objects.get(user=request.user)
       
        data = [ 
            ['Field', 'Value'],
            ['Borrow Date', now],
            ['User Id',request.user.id],
            ['Username', request.user.username],
            ['Full Name', request.user.get_full_name() or 'N/A'],
           
            ['Book ID', book.id],
            ['Book Title', book.book_name],
            ['Author', book.author],
            ['Return Date', formatted_return_date],
        ]

        # Create table
        table = Table(data, colWidths=[2.5 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))

        # Draw table
        table.wrapOn(p, width, height)
        table.drawOn(p, 80, height - 430)

        # Footer
        p.setFont("Helvetica-Oblique", 11)
        p.setFillColor(colors.grey)
        p.drawString(100, height - 460, "Thank you for using our library. Please return the book within the due date.")

        # Finalize PDF
        p.showPage()
        p.save()
        buffer.seek(0)


        # mail_subject="Collect Book"
        # message=render_to_string('mail.html',{
        #     'user':self.request.user,
           
            

        # })
        # to_email=self.request.user.email
        # send_email=EmailMultiAlternatives(mail_subject,'',to=[to_email])
        # send_email.attach_alternative(message,"text/html")
        # send_email.send()

        # return super().form_valid(form)

        # PDF response
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=borrow_receipt_{request.user.username}.pdf'
        return response
        
        


    else:
        return redirect('login')


def ReturnBook(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user.is_authenticated:
        try:
            borrow_instance = BorrowBooks.objects.get(user=request.user, book=book, is_returned=False)
        except BorrowBooks.DoesNotExist:
            messages.error(request, 'This book has already been returned or you have not borrowed it yet.')
            return redirect('profile')

        borrow_instance.is_returned = True
        borrow_instance.save()
        book.quantity += 1
        book.save()
        messages.success(request, f'You have successfully returned the book.')
        return redirect('profile')
    else:
        return redirect('login')



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # এটা User model-এ save করে
            # এখন Account model-এও save করতে হবে
            roll = form.cleaned_data.get('roll')
            reg = form.cleaned_data.get('reg')
            department = form.cleaned_data.get('department')
            session = form.cleaned_data.get('session')

            Account.objects.create(
                user=user,
                roll=roll,
                reg=reg,
                department=department,
                session=session
            )

            return redirect('login')  # বা আপনার পছন্দমতো page
    else:
        form = UserRegistrationForm()
    return render(request, 'sing.html', {'form': form})