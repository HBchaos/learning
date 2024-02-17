from django.shortcuts import render

# Create your views here.
# blog/views.py
from django.http import HttpResponseRedirect
from blogger.forms import CommentForm
from blogger.models import Post, Comment

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from blogger.forms import PostForm
from blogger.models import Post

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the current user
            post.save()
            return redirect('blog_index')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.author:  # Check if the current user is the author of the post
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user  # Set the author to the current user
                post.save()
                return redirect('blog_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/update_post.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def blog_index(request):
    posts = Post.objects.all().order_by("-publication_date")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)

# blog/views.py

# ...

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-publication_date")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

# blog/views.py

# ...

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                content=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }

    return render(request, "blog/details.html", context)
