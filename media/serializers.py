
from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'imdb_id', 'poster']
    
    def validate(self, data):
        user = self.context['request'].user

        # Ensure the user does not already have a movie with the same IMDb ID
        if Movie.objects.filter(user=user, imdb_id=data.get('imdb_id')).exists():
            raise serializers.ValidationError("You already have a movie with this IMDb ID.")

        return data