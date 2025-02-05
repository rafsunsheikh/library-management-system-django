from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import *
from django.http import request
from datetime import datetime, timedelta
from django.contrib import messages


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('library:home')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)




class UserLoginView(LoginView):
    template_name='library/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('library:home')

class InformationView(CreateView):
    template_name='library/information_form.html'
    model=InformationForm
    context_object_name="account_register"
    fields=['email', 'name', 'username', 'officer']
    success_url=reverse_lazy('library:login')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(InformationView, self).form_valid(form)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name='library/main.html'
    

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['accounts']=Account.objects.all()
        context['books'] = Book.objects.all()
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['books']=context['books'].filter(
                title__startswith=search_input)

        context['search_input']=search_input
        return context


class BookView(LoginRequiredMixin, ListView):
    model=Book
    context_object_name='books'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['books']=context['books']

        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['books']=context['books'].filter(
                title__startswith=search_input)

        context['search_input']=search_input

        return context



class BookCreate(LoginRequiredMixin, UserAccessMixin, CreateView):
    model=Book
    permission_required= 'books.add_books'
    fields='__all__'
    success_url=reverse_lazy('library:book-list')


    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(BookCreate, self).form_valid(form)



class BookDetail(LoginRequiredMixin, DetailView):
    model=Book
    context_object_name='book'
    template_name='library/book.html'


    


class BookUpdate(LoginRequiredMixin,UserAccessMixin,  UpdateView):
    model=Book
    permission_required = 'books.change_books'
    fields='__all__'
    success_url=reverse_lazy('library:book-list')


class BookDelete(LoginRequiredMixin,UserAccessMixin,  DeleteView):
    model=Book
    permission_required = 'books.delete_book'
    context_object_name='book'
    fields='__all__'
    success_url=reverse_lazy('library:book-list')



class officerView(LoginRequiredMixin, UserAccessMixin, ListView):
    model=Account
    context_object_name='officers'
    permission_required = 'officers.view_officers'
    template_name='library/officer_list.html'

    def get_context_data(self,  *args,**kwargs):
        context=super().get_context_data(**kwargs)
        context['officers']=context['officers'].exclude(is_admin=True)
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['officers']=context['officers'].filter(name__startswith=search_input)

        context['search_input']=search_input

        return context

class officerDetail(LoginRequiredMixin, DetailView):
    model=Account
    context_object_name='officer'
    template_name='library/officer.html'




class officerCreate(UserAccessMixin, CreateView):
    template_name = 'library/register.html'
    form_class = RegistrationForm
    permission_required = 'users.add_users'
    success_url = reverse_lazy('library:officer-list')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(officerCreate, self).form_valid(form)


class officerUpdate(LoginRequiredMixin, UpdateView):
    form_class = AccountUpdateForm
    template_name = 'library/officer_update.html'
    model = Account
    success_url=reverse_lazy('library:officer-list')
    

    def form_valid(self, form):
        user = form.save()
        return super(officerUpdate, self).form_valid(form)

class officerDelete(LoginRequiredMixin,UserAccessMixin,  DeleteView):
    model=Account
    template_name = 'library/officer_confirm_delete.html'
    permission_required = 'users.delete_users'
    context_object_name='officer'
    fields='__all__'
    success_url=reverse_lazy('library:officer-list')


class BorrowerView(LoginRequiredMixin, ListView):
    model=Borrower
    context_object_name='borrowers'
    template_name = 'library/borrower_list.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.user.is_admin or self.request.user.is_superuser:
            context['borrowers']=context['borrowers']
        else:
            context['borrowers']=context['borrowers'].filter(officer = self.request.user.id)


        return context



class BorrowerCreate(LoginRequiredMixin, UserAccessMixin, CreateView):
    model=Borrower
    permission_required= 'borrowers.add_borrowers'
    fields='__all__'
    success_url=reverse_lazy('library:borrower-list')

   #remember to get the object using slug or 404 
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        book = Book.objects.get(id=instance.book.id)
        officer = Account.objects.get(id=instance.officer.id)
        #get the book id from the form and check if the book is still available, then subtract.
        if book.available_copies > 0:
           book.available_copies -= 1
           book.save()
           instance.save()
           messages.success(self.request, "successful")
        messages.error(self.request, "Book not in stock")
        return redirect(reverse_lazy('library:borrower-list'))



class BorrowerDetail(LoginRequiredMixin,  DetailView):
    model=Borrower()
    context_object_name='borrower'
    template_name='library/borrower.html'
    


class BorrowerUpdate(LoginRequiredMixin,UserAccessMixin,  UpdateView):
    model=Borrower
    permission_required = 'borrowers.change_borrowers'
    fields='__all__'
    success_url=reverse_lazy('library:borrower-list')


class BorrowerDelete(LoginRequiredMixin,UserAccessMixin,  DeleteView):
    model=Borrower
    permission_required = 'borrowers.delete_borrowers'
    context_object_name='borrower'
    fields='__all__'
    success_url=reverse_lazy('library:borrower-list')


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        book = Book.objects.get(id=self.object.book.id)
        book.available_copies +=1
        book.save()
        self.object.delete()
        return redirect('library:borrower-list')