# Ваше приложение/views.py
import jwt
from django.http import HttpResponseForbidden
from jwt import algorithms
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import PostForm
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.middleware.csrf import get_token
import json
from django.shortcuts import get_object_or_404
import jwt
from datetime import datetime, timedelta
from rest_framework.serializers import ValidationError
from rest_framework import serializers
from .models import Post, Like


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.data, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            token = request.COOKIES.get("jwt_token")
            try:
                payload = jwt.decode(token, 'django-insecure-bq+wz_eh4(u70xtj^gskca@nu17!#0g8+_ip0z!b(x_7!+scb8',
                                     algorithms=['HS256'])
                print(payload)
                user_id = payload['user_id']
                user = User.objects.get(pk=user_id)  # Получаем объект пользователя по его идентификатору
                print(user)
                post.author = user
                post.save()
                print(post)
            except jwt.ExpiredSignatureError:
                return HttpResponseForbidden('JWT token has expired')

            return Response({'message': 'Post created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            # Возвращаем ошибку валидации
            raise ValidationError({'message': 'Error creating post. Please check the form.'})

    return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Проверка, существует ли уже лайк от данного пользователя для этого поста
    existing_like = Like.objects.filter(user=user, post=post).first()

    if existing_like:
        # Если лайк уже существует, удалите его
        existing_like.delete()
        message = 'Like removed successfully.'
    else:
        # Если лайка нет, создайте новый
        Like.objects.create(user=user, post=post)
        message = 'Like added successfully.'

    return Response({'message': message})


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.count_likes()

    def get_comments_count(self, obj):
        return obj.comment_set.count()