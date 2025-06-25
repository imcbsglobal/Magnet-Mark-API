from rest_framework import serializers
from .models import CceEntry, MarkAPIUser


class MarkAPIUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkAPIUser
        fields = ['user_id', 'last_synced_at']


class CceEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CceEntry
        fields = [
            'slno',
            'mark',
            'last_updated'
        ]
