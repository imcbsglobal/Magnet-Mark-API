from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now, is_naive, make_aware, localtime
from django.db.models import Max
from .models import MarkAPIUser, CceEntry
from .serializers import CceEntrySerializer
from .protection import generate_token, token_required
from rest_framework.pagination import LimitOffsetPagination

# HEATH CHECK VIEW


class HealthCheckView(APIView):
    def get(self, request):
        return Response({
            "status": "ok",
            "service": "Magnet Safa Mark Sync API",
            "message": "Welcome to the Magnet Safa School Sync API. Use your PASSWORD and user ID to login and fetch updated student marks.",
            "version": "v1.0",
            "timestamp": now(),
            "routes": {
                "health": "/api/health/",
                "login": "/api/login/",
            }
        }, status=status.HTTP_200_OK)


# LOGIN VIEW
class LoginView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        if not user_id or not password:
            return Response({"error": "Missing user_id or password"}, status=400)

        try:
            user = MarkAPIUser.objects.get(
                user_id=user_id, password=password)
        except MarkAPIUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        token = generate_token(user_id)

        return Response({
            "message": "Login successful",
            "token": token,
            "user_id": user.user_id
        }, status=200)


# MARK FETCHING VIEW
class MarkSyncAPIView(APIView):
    @token_required
    def get(self, request):
        user = request.mark_user
        user_id = request.user_id

        try:
            user = MarkAPIUser.objects.get(user_id=user_id)
        except MarkAPIUser.DoesNotExist:
            return Response({"error": "Invalid user"}, status=401)

        # Fetch last synced time
        last_sync = user.last_synced_at

        if last_sync and is_naive(last_sync):
            last_sync = make_aware(last_sync)

        if last_sync:
            queryset = CceEntry.objects.filter(last_updated__gt=last_sync)
        else:
            queryset = CceEntry.objects.all()

        total_count = queryset.count()
        latest_updated = queryset.aggregate(
            latest=Max('last_updated'))['latest']

        # 🛠️ Make latest_updated timezone-aware
        if latest_updated and is_naive(latest_updated):
            latest_updated = make_aware(latest_updated)

        # Apply pagination
        paginator = LimitOffsetPagination()
        paginated_qs = paginator.paginate_queryset(
            queryset.order_by('last_updated'), request)

        serialized = CceEntrySerializer(paginated_qs, many=True)

        # Update user's last_synced_at
        if latest_updated:
            user.last_synced_at = latest_updated
            user.save(update_fields=['last_synced_at'])

        return paginator.get_paginated_response({
            "status": "success",
            "user": user_id,
            "total_entries": total_count,
            "sync_period": {
                "from": localtime(last_sync) if last_sync else None,
                "to": localtime(latest_updated) if latest_updated else None
            },
            "data": serialized.data
        })
