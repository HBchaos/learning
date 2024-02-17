from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):
        return self.title


# class User(models.Model):
#     user_name = models.CharField(max_length=30)
#     bio = models.CharField(max_length=255)


# blog/models.py

# ...

class Comment(models.Model):
    author = models.CharField(max_length=60)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"


