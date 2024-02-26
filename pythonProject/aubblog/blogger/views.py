from django.shortcuts import render

# Create your views here.
# blog/views.py
from django.http import HttpResponseRedirect
from blogger.forms import CommentForm, LoginForm
from blogger.models import Post, Comment
from django.contrib.auth import login, authenticate
from . import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from blogger.forms import PostForm, LoginForm
from blogger.models import Post

class register_page(generic.CreateView):
    form_class = UserCreationForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("login")

@login_required
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
            else:
                message = 'Login failed!'
    return render(
        request, 'blog/login.html', context={'form': form, 'message': message})

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
