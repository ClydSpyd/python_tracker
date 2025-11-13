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

    # Write-only PK field that maps to the FK
    space_id = serializers.PrimaryKeyRelatedField(
        source='space',
        queryset=Space.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,   # allow clearing the relation with null
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'resourceLinks', 'updates', 'tags',
            'status', 'createdAt', 'space', 'space_id', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['user', 'createdAt', 'updated_at', 'completed_at']