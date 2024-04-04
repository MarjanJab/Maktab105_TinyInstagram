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
from .models import Follow



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

    def setup(self, request, *args, **kwargs):
        self.next= request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'Your have already login!', 'success')
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)

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
                if self.next:
                    return redirect(self.next)
                return redirect('post:home')
            messages.error(request, 'username or password is incorrect', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You were logged successfully!', 'success')
        return redirect('post:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'user/profile-edit.html'

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.user_posts.all()
        relation = Follow.objects.filter(follower=request.user ,following=user)
        if relation.exists():
            is_following = True
        return render(request, self.template_name, {'user': user, 'posts': posts, 'is_following': is_following})


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


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk= user_id)
        following = Follow.objects.filter(follower=request.user , following=user)
        if following.exists():
            messages.error(self.request, 'You have already followed this user!','error')
        else:
            Follow(follower=request.user, following=user).save()
            messages.success(self.request, 'You followed this user!','success')
        return redirect('user:user_profile', user.id)


class UserUnfollowView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(pk= user_id)
        relation =Follow.objects.filter(follower=request.user ,following=user)
        if relation.exists():
            relation.delete()
            messages.success(self.request, 'You can unfollow this user!','success')
        else:
            messages.error(self.request, 'You have not Followed this user!','error')

        return redirect('user:user_profile', user.id)
