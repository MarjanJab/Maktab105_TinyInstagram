from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views import View


# Create your views here.



class HomeView(View):

    def get(self,request, *args, **kwargs):
        return render(request, 'base.html')

    def post(self,request,*args,**kwargs):
        return render(request,'base.html')