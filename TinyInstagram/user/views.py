from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'user/register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password2'])
            messages.success(request, 'Your were registered successfully!','success')
            return redirect('home')
        return render(request,self.template_name,{'form':form})



class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
       form = self.form_class(request.POST)
       if form.is_valid():
           cd = form.cleaned_data
           user = authenticate(request, username=cd['username'],password=cd['password'])
           if user is not None:
               login(request, user)
               messages.success(request, 'Your logged in successfully!','success')
               return redirect('home')
           messages.error(request, 'username or password is incorrect','warning')
       return render(request,self.template_name,{'form':form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You were logged successfully!','success')
        return redirect('home')