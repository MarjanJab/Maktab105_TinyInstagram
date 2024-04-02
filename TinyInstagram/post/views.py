from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView
from django.views import View
from .models import Post
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpsertForm


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


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpsertForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post =  self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'You do not have permission to update this post', 'danger')
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post =  self.post_instance
        form =  self.form_class(instance=post)
        return render(request, 'home/update_post.html', {'form':form})

    def post(self, request ,*args, **kwargs):
        post =  self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['content'][:30])
            new_post.save()
            messages.success(request, 'your post has been updated successfully!', 'success')
            return redirect('post:post_detail', new_post.id , new_post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpsertForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html' ,{'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['content'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'your post has been created successfully!', 'success')
            return redirect('post:post_detail', new_post.id, new_post.slug)



