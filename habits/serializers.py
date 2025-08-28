from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Map snake_case to camelCase
        if 'color_scheme' in data:
            data['colorScheme'] = data.pop('color_scheme')
        return data

class HabitWithRecordsSerializer(serializers.ModelSerializer):
    records = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'target', 'icon', 'created_at', 'updated_at', 'user', 'records', 'color_scheme']

    def get_records(self, obj):
        return [record.date for record in obj.records.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Map snake_case to camelCase
        if 'color_scheme' in data:
            data['colorScheme'] = data.pop('color_scheme')
        return data