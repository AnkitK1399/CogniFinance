from rest_framework import serializers
from .models import AISummary

class AISummarySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = AISummary
        fields = ['id', 'ai_summary', 'created_at']