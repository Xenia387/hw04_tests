from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User
from .forms import PostForm
from .utils import paginat


def index(request):
    post_list = Post.objects.all()
    page_obj = paginat(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_posts = group.posts.all()
    page_obj = paginat(request, group_posts)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    author_posts = user.posts.all()
    page_obj = paginat(request, author_posts)
    context = {
        'author': user,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    context = {'form': form}
    if not form.is_valid():
        return render(request, 'posts/post_create.html', context)
    else:
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        context = {'form': form, 'is_edit': True}
        if not form.is_valid():
            return render(request, 'posts/post_create.html', context)
        else:
            form.save()
            return redirect('posts:post_detail', post.pk)
    return render(request, 'posts/post_detail.html', context)
