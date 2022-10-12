from .models import Post
from django.forms import ModelForm

class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']