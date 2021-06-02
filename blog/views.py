import json

import requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.models import Site
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core import settings
from users.utils import user_from_token
from .forms import PostForm
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer

path = str(Site.objects.get(id=settings.SITE_ID))
headers = {'Content-Type': 'application/json'}


class PostListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/home.html'

    def get(self, request, *args, **kwargs):
        response = requests.get(
            path + 'api/posts/',
            headers=headers,
            data=request.data
        )
        output = response.json()
        return Response(template_name='blog/home.html', data={
            "posts": output,
        })


class PostDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/post_detail.html'

    def get(self, request, pk):
        token = request.COOKIES.get('token')
        username = ""
        response = requests.get(
            path + 'api/posts/' + str(pk),
            headers=headers,
            data=request.data
        )
        if user_from_token(token=token):
            username = user_from_token(token=token).username
        output = response.json()
        return Response(data={
            'post': output,
            'user': username
        })


class PostCreateView(APIView):
    model = Post
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/post_form.html'

    def get(self, request, *args, **kwargs):
        return Response(template_name='blog/post_form.html', data={
            "form": PostForm
        })

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        form_data = {
            "title": request.data.get("title"),
            "content": request.data.get("content"),
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        requests.post(
            path + 'api/posts/',
            headers=headers,
            data=json.dumps(form_data))

        return redirect('blog-home')


class PostUpdateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return Response(template_name='blog/post_form.html', data={
            "form": form
        })

    def post(self, request, pk, *args, **kwargs):
        token = request.COOKIES.get('token')
        form_data = {
            "title": request.data.get("title"),
            "content": request.data.get("content"),
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        requests.put(
            path + 'api/posts/' + str(pk) + '/',
            headers=headers,
            data=json.dumps(form_data)
        )

        return redirect('blog-home')


class PostDeleteView(APIView):
    model = Post
    success_url = '/'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, *args, **kwargs):
        token = request.COOKIES.get('token')
        form_data = {
            "title": request.data.get("title"),
            "content": request.data.get("content"),
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        response = requests.get(
            path + 'api/posts/' + str(pk) + '/',
            headers=headers,
            data=json.dumps(form_data))

        output = response.json()
        return Response(template_name='blog/post_confirm_delete.html', data={
            "post": output
        })

    def post(self, request, pk, *args, **kwargs):
        token = request.COOKIES.get('token')
        requests.delete(
            path + 'api/posts/' + str(pk) + '/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            data=json.dumps({'data': "None"})
        )
        return redirect('blog-home')


class AboutView(DetailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'blog/about.html', {'title': 'About'})
