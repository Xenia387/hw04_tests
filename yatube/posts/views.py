from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
# from django.views.decorators.cache import cache_page

from .forms import Comment, CommentForm, PostForm
from .models import Group, Post, User
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
    form_comment = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post_id)
    context = {
        'post': post,
        'form_comment': form_comment,
        'comments': comments,
    }
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
    form = PostForm(
        request.POST or None,
        instance=post,
    )
    context = {
        'form': form,
        'is_edit': True,
    }
    if post.author == request.user:
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post.pk)
        return render(request, 'posts/post_create.html', context)
    return render(request, 'posts/post_detail.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'form': form,
    }
    if not form.is_valid():
        return render(request, 'posts/add_comment.html', context)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', id=post_id)
