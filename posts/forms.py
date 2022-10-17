from .models import Post
from django.forms import ModelForm
from django.views.generic import UpdateView

class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        
class UpdatePost(UpdateView):
    class Meta:
        model = Post
        fields = ['text', 'group']