from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.middleware.csrf import get_token
import json
import jwt
from datetime import datetime, timedelta


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class YourModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            # Получение CSRF-токена
            csrf_token = get_token(request)

            user = authenticate(request, username=username, password=password)
            print(username, password)
            if user is not None:
                login(request, user)
                # Вход успешен, выполните необходимые действия

                payload = {
                    'user_id': user.id,
                    'username': user.username,
                    'exp': datetime.utcnow() + timedelta(days=7),  # Пример: токен действителен 1 день
                }
                jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                response = JsonResponse({'jwt_token': jwt_token, 'csrf_token': csrf_token})
                response.set_cookie('jwt_token', jwt_token, httponly=True, secure=True)
                return response
            else:
                # Ошибка входа, обработайте соответственно
                return HttpResponse('Login failed', status=400)
        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON format', status=400)

    return JsonResponse({'message': 'Invalid request'})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Регистрация успешна, выполните необходимые действия
            return
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def some_protected_view(request):
    # Ваш код для защищенного представления
    return render(request, 'protected_view.html')


class RegisterUserView(APIView):
    def post(self, request, format=None):
        form = UserCreationForm(request.data)
        print(request.data)
        print(form)
        print(get_token(request))
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return JsonResponse({'message': 'somthing wrong'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_info(request):
    if request.method == 'GET':
        try:
            # Получение данных JSON из тела запроса

            token = request.COOKIES.get("jwt_token")
            try:
                payload = jwt.decode(token, 'django-insecure-bq+wz_eh4(u70xtj^gskca@nu17!#0g8+_ip0z!b(x_7!+scb8',
                                     algorithms=['HS256'])
                return JsonResponse(payload)
            except jwt.ExpiredSignatureError:
                return HttpResponseForbidden('JWT token has expired')
            print(payload)


        except jwt.InvalidTokenError:
            return HttpResponseForbidden('Invalid JWT token')


'''
    auth_header = request.headers.get('Authorization', '')
    if ' ' in auth_header:
        # Если в строке есть пробел, попробуем разделить строку
        # по пробелу и проверить формат
        auth_type, jwt_token = auth_header.split(' ', 1)

        if auth_type.lower() == 'bearer':
            try:
                payload = jwt.decode(jwt_token, 'your-secret-key', algorithms=['HS256'])
                user_id = payload.get('user_id')

                try:
                    user = User.objects.get(id=user_id)
                    return JsonResponse({'username': user.username, 'email': user.email})
                except User.DoesNotExist:
                    return JsonResponse({'message': 'User not found'}, status=404)

            except jwt.ExpiredSignatureError:
                return HttpResponseForbidden('JWT token has expired')
            except jwt.InvalidTokenError:
                return HttpResponseForbidden('Invalid JWT token')
        else:
            return HttpResponseForbidden('Unsupported authorization type')
    else:
        return HttpResponseForbidden('No JWT token provided')

'''
