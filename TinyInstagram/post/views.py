from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView
from django.views import View
from .models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.



class HomeView(View):

    def get(self,request, *args, **kwargs):
        posts = Post.objects.all()
        return render(request, 'home/home.html', {'posts': posts})


class PostDetailView(View):
    def get (self, request, post_id, post_slug):
        post = Post.objects.get(pk = post_id, slug = post_slug)
        return render(request, 'home/detail_post.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id ):
        post = Post.objects.get(pk = post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully!', 'success')
        else:
            messages.error(request, 'You do not have permission to delete this post.', 'danger')
        return redirect('post:home')