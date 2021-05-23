from django.urls import path
from . import views
from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostApiListView, \
    PostApiDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path("api/posts", PostApiListView.as_view(), name="all-posts"),
    path('api/posts/<int:pk>/', PostApiDetailView.as_view()),

]
