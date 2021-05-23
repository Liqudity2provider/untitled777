from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserList, UserDetail

urlpatterns = [
    path("users", UserList.as_view(), name="all-users"),
    path('users/<int:pk>/', UserDetail.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
