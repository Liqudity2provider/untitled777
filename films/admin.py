from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse, HttpResponse
from django.urls import reverse, path
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from .forms import CommentAdminDeleteForm
from .models import Film, Genre, Comment

# Register your models here.
from django.contrib import admin
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.roles import get_user_roles

from core.roles import FilmModerator
from .views import UpdateFilmList, FilmDetailView

"""
Create group with next permissions:
blog-category-Can Add Category
blog-category-Can View Category
films-comment-Can Change Comment
films-comment-Can Delete Comment
films-comment-Can View Comment
films-category-Can Add Category
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
    list_display_links = ['name']

    def film_comments(self, obj):
        info = (self.model._meta.app_label, 'comment')
        href = '/%s/%s/%s/' % ((self.admin_site.name,) + info)

        return format_html(
            f"<a href='{href}?film_id={obj.id}'> Comments </a>"
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
            return ['name', 'image', 'link', 'rating', 'genres']
        else:
            return ['name', 'image', 'link', 'rating', 'genres']


admin.site.register(Film, FilmAdmin)

admin.site.register(Genre)


class CommentAdmin(MPTTModelAdmin):
    list_display = ['content', 'film', 'author', 'deleted', 'delete_comment']
    change_form_template = 'custom_change_form.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('delete_comment_view/<int:pk>/', self.delete_comment_view, name='delete_comment_view'),
        ]
        return my_urls + urls

    def delete_comment(self, obj):
        return format_html(
            f'<a class="button" href="{reverse("admin:delete_comment_view", kwargs={"pk": obj.pk})}"> Delete </a>&nbsp;'
        )

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['film', 'author', 'parent', 'content', 'deleted', 'reason_for_deleting']
        if obj.deleted:
            return ['reason_for_deleting']
        return ['film', 'author', 'parent', 'content']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif has_role(request.user, FilmModerator):
            return ['film', 'author', 'parent', 'content']
        else:
            return self.fields

    def get_queryset(self, request):
        film_id = request.GET.get('film_id')
        if film_id:
            request.GET._mutable = True

            return Film.objects.get(pk=film_id).comments
        return Comment.objects.all()

    def delete_comment_view(self, request, pk):
        if request.method == 'POST':
            form = CommentAdminDeleteForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.get(pk=pk)
                comment.reason_for_deleting = form.data['reason_for_deleting']
                comment.save()
                comment.delete()

                info = (self.model._meta.app_label, 'comment')
                href = '/%s/%s/%s/' % ((self.admin_site.name,) + info)
                return redirect(href)

        form = CommentAdminDeleteForm()
        return render(request, 'delete_comment_view.html', {
            'form': form,
            'pk': pk
        })


admin.site.register(Comment, CommentAdmin)
