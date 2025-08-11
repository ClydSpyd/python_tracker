
from rest_framework import serializers
from .models import FocusItem

class FocusItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusItem
        fields = ['id', 'title', 'description', 'icon', 'week_starting']

    def validate(self, data):
        user = self.context['request'].user

        # ✅ Only check the limit when creating a new item
        if self.instance is None and user.focus_items.count() >= 3:
            raise serializers.ValidationError("You can only have up to 3 focus items.")

        return data
