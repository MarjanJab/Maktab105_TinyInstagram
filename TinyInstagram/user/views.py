from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views import View
from .forms import UserRegisterationForm
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
class RegisterView(View):
    form_class = UserRegisterationForm
    template_name = 'user/register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(request, 'Your were registered successfully!','success')
            return redirect('home')
        return render(request,self.template_name,{'form':form})



