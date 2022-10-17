from django.shortcuts import render, get_object_or_404, redirect
from groups.models import Group
from .models import Post, User
from .forms import CreatePost, UpdatePost
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
       )


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    
    return render(
        request,
        "group.html",
        {"group": group, "page": page, 'paginator': paginator}
        )

@login_required
def new_post(request):
    form = CreatePost(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})

@login_required
def profile(request, username):
    current_user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=current_user)
    total_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {"current_user": current_user,"page": page, 'paginator': paginator, 'total': total_posts})
 
@login_required
def post_view(request, username, post_id):
    current_user = User.objects.get(username=username)
    total_posts = Post.objects.filter(author=current_user).count()
    current_post = Post.objects.get(pk=post_id)
    return render(request, 'post.html', {"current_user": current_user, "current_post": current_post,'total': total_posts})

@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if post.author != request.user:
        return redirect('post', username=post.author, post_id=post.id )
    form = CreatePost(request.POST or None, instance=post)       
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(
                'post',
                username=username,
                post_id=post_id
                )
    return render(request, 'new_post.html', {'form': form, 'post': post})