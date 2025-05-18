from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import BookForm,CommentForm
from .models import Book,Comment
from . import forms
from . import models  
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class AddBook(CreateView):
    form_class = forms.BookForm  
    model =models.Book
    success_url = reverse_lazy('addbooks')  
    template_name = 'add_books.html'  

    # def form_valid(self, form):
    #     return super().form_valid(form)

    def form_valid(self, form):
        book_name = form.cleaned_data['book_name']
        author = form.cleaned_data['author']
        # price = form.cleaned_data['price']
        quantity = form.cleaned_data['quantity']

        # check if book already exists (same name & author)
        existing_book = models.Book.objects.filter(book_name=book_name, author= author).first()

        if existing_book:
            # Update quantity if exists
            existing_book.quantity += quantity
            existing_book.save()
            messages.success(self.request, f"{quantity} more copies of '{book_name}' added.")
            return redirect(self.success_url)
        else:
            # Otherwise create new book
            messages.success(self.request, f"Book '{book_name}' added successfully.")
            return super().form_valid(form)
    
    
    

# class DetailsBookView(DetailView):
#     model = Book
#     pk_url_kwarg = 'id'
#     template_name = 'book_details.html'

#     def post(self, request, *args, **kwargs):
#         car = self.get_object()
#         comment_form = CommentForm(data=request.POST)
        
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.car = car
#             new_comment.save()
#             return redirect('details_book', id=car.id)  # Redirect after POST to avoid form resubmission
        
#         context = self.get_context_data()
#         context['comment_form'] = comment_form  # Include the form with validation errors
#         return self.render_to_response(context)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         car = self.object
#         comments = car.comments.all()
#         comment_form = CommentForm()
        
#         context['comments'] = comments
#         context['comment_form'] = comment_form
        
#         return context
    
class DetailsBookView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'    

    def post(self, request, *args, **kwargs):
        book = self.get_object()  # Get the current Book object
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book  # Associate comment with the book
            new_comment.save()
            return redirect('details_book', id=book.id)  # Redirect after POST to avoid form resubmission
        
        context = self.get_context_data()
        context['comment_form'] = comment_form  # Include the form with validation errors
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object  # The Book object being viewed
        comments = book.comments.all()  # Get all comments related to the book
        comment_form = CommentForm()  # Empty comment form
        
        context['comments'] = comments
        context['comment_form'] = comment_form  # Include form in context
        
        return context

