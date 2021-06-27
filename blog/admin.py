from django.contrib import admin
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.roles import get_user_roles

from core.roles import PostModerator
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    """
    Create group with next permissions:
    auth-user-EDIT POST WITHOUT AUTHOR
    blog-post-Can Change Post
    blog-post-Can View Post

    Users from this group can edit content in Post (but cant edit author)
    """

    # list_display = ['pk', 'title', 'category']
    list_display = ['pk', 'title']
    list_editable = []
    # list_editable = ['category']
    # fields = ['title', 'content', 'category', 'image', 'video', 'author', 'date_posted']
    # fields = ['title', 'content', 'image', 'video', 'author', 'date_posted']
    fields = ['title', 'content', 'author', 'date_posted', 'd']
    list_display_links = ['pk', 'title', ]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif has_role(request.user, PostModerator):
            return ['author']
        else:
            # return ['title', 'content', 'category', 'image', 'video', 'author', 'date_posted']
            return ['title', 'content', 'category', 'author', 'date_posted']


admin.site.register(Post, PostAdmin)

admin.site.register(Category)
