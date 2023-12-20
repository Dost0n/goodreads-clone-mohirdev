from django.shortcuts import render, redirect
from django.views import View
from users.models import CustomUser
from users.forms import UserCreateForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class RegisterView(View):

    def get(self, request):
        create_form = UserCreateForm()

        context = {
            'form':create_form
        }
        return render(request, 'register.html', context)
    
    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('users:login_page')
        else:

            context = {
                'form':create_form
                }
            return render(request, 'register.html', context)


class LoginView(View):

    def get(self, request):
        login_form = AuthenticationForm()

        context = {
            'form':login_form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have done successfully loggen in.")
            return redirect("books:book-list")
        else:
            context = {
                'form':login_form
            }
            return render(request, 'register.html', context)


class Profile(LoginRequiredMixin,View):
    def get(self, request):
        context = {
            'user':request.user
        }
        return render (request, 'profile.html',context)


class ProfileUpdate(LoginRequiredMixin,View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        context = {
            'form':form
        }
        return render (request, 'profile_edit.html',context)

    def post(self, request):
        form = UserUpdateForm(instance=request.user,
                              data=request.POST,
                              files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "You successfully update data")
            return redirect('users:profile_page')
        else:
            context = {
                'form':form
                }
            return render(request, 'profile_edit.html', context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You successfully logout')
        return redirect('books:book-list')