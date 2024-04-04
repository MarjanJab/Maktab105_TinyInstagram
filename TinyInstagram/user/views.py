from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from post.models import Post


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'user/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # form.save()
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password2'])
            messages.success(request, 'Your were registered successfully!', 'success')
            return redirect('post:home')
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'Your have already registered!', 'success')
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Your logged in successfully!', 'success')
                return redirect('post:home')
            messages.error(request, 'username or password is incorrect', 'warning')
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'Your have already login!', 'success')
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You were logged successfully!', 'success')
        return redirect('post:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'user/profile-edit.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, self.template_name, {'user': user, 'posts': posts})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'user/password_reset_form.html'
    success_url = reverse_lazy('user:password_reset_done')
    email_template_name = 'user/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('user:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'
