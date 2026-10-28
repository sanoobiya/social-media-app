"""
URL configuration for social_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from social_media.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',RegisterView.as_view()),
    path('token',obtain_auth_token),
    path('posts/',PostListCreateView.as_view()),
    path('posts/<int:pk>/',PostDetailView.as_view()),
    path('comments/',CommentListCreateView.as_view()),
    path('likes/',LikeListCreateView.as_view()),
    path('likes/<int:pk>/',LikeDeleteView.as_view()),
    path('follow/',FollowListCreateView.as_view()),
    path('unfollow/<int:pk>/',UnfollowView.as_view())
]
