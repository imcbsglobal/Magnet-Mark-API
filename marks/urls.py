from django.urls import path
from .views import HealthCheckView, LoginView, MarkSyncAPIView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('login/', LoginView.as_view(), name='login'),
    path('mark-sync/', MarkSyncAPIView.as_view(), name='mark-sync')
]
