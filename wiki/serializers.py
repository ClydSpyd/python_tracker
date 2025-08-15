
from rest_framework import serializers
from .models import Movie, Series, Quote

class MediaBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'title', 'year', 'released', 'runtime', 'genre', 'director', 'actors',
            'plot', 'language', 'poster_url', 'metascore', 'imdb_rating', 'imdb_votes',
            'imdb_id', 'ratings', 'created_at'
        ]
        abstract = True

class MovieSerializer(MediaBaseSerializer):
    class Meta(MediaBaseSerializer.Meta):
        model = Movie

class SeriesSerializer(MediaBaseSerializer):
    class Meta(MediaBaseSerializer.Meta):
        model = Series


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['content', 'author', 'additional_info', 'year', 'created_at']

    def validate(self, data):
        user = self.context['request'].user

        # Ensure the user does not already have a quote with the same content and author
        if Quote.objects.filter(user=user, content=data.get('content'), author=data.get('author')).exists():
            raise serializers.ValidationError("You already have a quote with this quote and author.")

        return data