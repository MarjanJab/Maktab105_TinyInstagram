from django import forms
from .models import Post


class PostCreateUpsertForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', )