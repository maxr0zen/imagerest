"""
URL configuration for imagerest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from users.views import RegisterUserView, login_view, user_info, UnsubscribeAPIView, SubscribeAPIView
from posts.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api/token', obtain_auth_token, name='token_obtain_pair'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', login_view),
    path('api/user-info/', user_info, name='user_info'),
    path('post_create/', create_post, name='create_post'),
    path('toggle-like/<int:post_id>/', toggle_like, name='toggle_like'),
    path('post/<int:pk>/', get_post_details, name='post_detail'),
    path('post/<int:pk>/add-comment/', add_comment, name='add_comment'),
    path('subscribe/<int:user_id>/', SubscribeAPIView.as_view(), name='subscribe'),
    path('unsubscribe/<int:user_id>/', UnsubscribeAPIView.as_view(), name='unsubscribe'),
    path('user/feed/', get_user_feed, name='user_feed'),  # лента с его постами
    path('user/posts/', UserPostsAPIView.as_view(), name='user_posts'),  # лента с постами тех, на кого подписан user
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
