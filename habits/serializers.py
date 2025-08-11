from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class HabitWithRecordsSerializer(serializers.ModelSerializer):
    records = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'target', 'icon', 'created_at', 'updated_at', 'user', 'records']

    def get_records(self, obj):
        return [record.date for record in obj.records.all()]
