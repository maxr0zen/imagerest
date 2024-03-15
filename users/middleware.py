import jwt
from django.http import HttpResponseForbidden
from django.conf import settings
from datetime import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class YourJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        print(jwt_token)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
                # Добавьте дополнительные проверки, если необходимо
                # Например, проверка наличия пользователя в базе данных
                # или проверка срока действия токена

                # Поместите информацию о пользователе в request
                request.username = payload.get('username')
            except ExpiredSignatureError:
                return HttpResponseForbidden('JWT token has expired')
            except InvalidTokenError:
                return HttpResponseForbidden('Invalid JWT token')

        response = self.get_response(request)
        return response