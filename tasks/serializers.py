from rest_framework import serializers
from .models import Task
from spaces.models import Space  # Adjust import if needed

class SpaceSummarySerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Space
        fields = ['id', 'title', 'description', 'createdAt']

class TaskSerializer(serializers.ModelSerializer):
    resourceLinks = serializers.JSONField(source='resource_links', required=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    space = SpaceSummarySerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'resourceLinks', 'updates', 'tags',
            'status', 'createdAt', 'space'
        ]
        read_only_fields = ['user', 'createdAt', 'updated_at', 'completed_at']