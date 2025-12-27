from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Map snake_case to camelCase
        if 'color_scheme' in data:
            data['colorScheme'] = data.pop('color_scheme')
        if 'enabled_at' in data:
            data['enabledAt'] = data.pop('enabled_at')
        if 'disabled_at' in data:
            data['disabledAt'] = data.pop('disabled_at')
        return data

class HabitWithRecordsSerializer(serializers.ModelSerializer):
    records = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'target', 'icon', 'created_at', 'enabled_at', 'disabled_at', 'user', 'records', 'color_scheme']

    def get_records(self, obj):
        return [record.date for record in obj.records.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Map snake_case to camelCase
        if 'color_scheme' in data:
            data['colorScheme'] = data.pop('color_scheme')
        if 'enabled_at' in data:
            data['enabledAt'] = data.pop('enabled_at')
        if 'disabled_at' in data:
            data['disabledAt'] = data.pop('disabled_at')
        return data