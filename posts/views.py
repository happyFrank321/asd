from django.shortcuts import render, get_object_or_404, redirect
from groups.models import Group
from .models import Post
from .forms import CreatePost
from django.contrib.auth.decorators import login_required

def index(request):
    latest = Post.objects.order_by("-pub_date")[:11]
    return render(request, "index.html", {"posts": latest})


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})

@login_required
def new_post(request):
    error = ''
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index')
        else:
            error = 'Форма была неверной'
            
    form = CreatePost()
    data = {
        'form': form,
        'error': error
    }
    return render(request, "new_post_form.html",data)
