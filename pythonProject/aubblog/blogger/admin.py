from django.contrib import admin

# Register your models here.
# blog/admin.py
from django import forms
from blogger.models import Category, Comment, Post

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']

class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # For creation of a new post
            kwargs['form'] = PostAdminForm
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

# admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

# class PostAdmin(admin.ModelAdmin):
#     pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)