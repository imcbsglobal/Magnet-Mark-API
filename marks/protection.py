import jwt
from django.conf import settings
from rest_framework.response import Response
from functools import wraps
from .models import MarkAPIUser


def generate_token(user_id):
    payload = {
        "user_id": user_id
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token


def token_required(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"error": "Authorization header missing or malformed."}, status=401)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("user_id")

            # Validate user existence
            user = MarkAPIUser.objects.get(user_id=user_id)

            # Attach user object and user_id to the request (custom fields)
            setattr(request, "mark_user", user)
            setattr(request, "user_id", user_id)

        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return Response({"error": "Invalid or expired token."}, status=401)
        except MarkAPIUser.DoesNotExist:
            return Response({"error": "Invalid user."}, status=401)

        return view_func(self, request, *args, **kwargs)

    return wrapped_view
