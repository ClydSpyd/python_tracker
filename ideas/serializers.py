from rest_framework import serializers
from .models import Idea

class IdeaSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Idea
        fields = ['id', 'title', 'tags', 'createdAt']
        read_only_fields = ['createdAt', 'id']