from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from .models import Film, Genre, Comment

# Register your models here.
from django.contrib import admin
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.roles import get_user_roles

from core.roles import FilmModerator
from .views import UpdateFilmList, FilmDetailView

"""
Create group with next permissions:
films-comment-Can Change Comment
films-comment-Can Delete Comment
films-comment-Can View Comment
films-film-Can Change Film
films-film-Can View Film

Users from this group can:
1. add new Film models (using parsing utils)
2. edit Film content (description, rating, genres)
3. can delete comments and add a reason for deleting
"""


class FilmAdmin(admin.ModelAdmin):

    list_display = ['name', 'rating', 'film_actions', 'film_comments']
    list_editable = ['rating']
    fields = ['name', 'description', 'image', 'link', 'rating', 'genres']
    readonly_fields = []
    list_display_links = ['name']

    def film_comments(self, obj):
        return format_html(
            f"<a href='/admin/films/comment/?e={obj.id}'> Comments </a>"
        )

    def film_actions(self, obj):
        return format_html(
            f'<a class="button" href="{reverse("film-detail", kwargs={"pk": obj.pk})}">Detail</a>&nbsp;'
            f'<a class="button" href="{reverse("update-db")}">Update</a>',
        )

    film_actions.short_description = 'Film Actions'
    film_actions.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif has_role(request.user, FilmModerator):
            return ['image', 'name', 'link']
        else:
            return ['name', 'image', 'link', 'rating', 'genres']


admin.site.register(Film, FilmAdmin)

admin.site.register(Genre)


class CommentAdmin(MPTTModelAdmin):

    list_display = ['content', 'film', 'author', 'deleted']
    fields = []
    readonly_fields = []

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['film', 'author', 'parent', 'content', 'deleted']
        if obj.deleted:
            return ['reason_for_deleting']
        return ['film', 'author', 'parent', 'content', 'deleted']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif has_role(request.user, FilmModerator):
            return ['film', 'author', 'parent', 'content']
        else:
            return self.fields

    def get_queryset(self, request):
        e = request.GET.get('e')
        if e:
            return Film.objects.get(pk=e).comments
        return Comment.objects.all()


admin.site.register(Comment, CommentAdmin)
