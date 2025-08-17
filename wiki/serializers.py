from rest_framework import serializers
from .models import Movie, Series, Quote, Book, Link, PinnedItem

class MediaBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id','title', 'year', 'released', 'runtime', 'genre', 'director', 'actors',
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
        fields = ['id', 'content', 'author', 'additional_info', 'year', 'created_at']

    def validate(self, data):
        user = self.context['request'].user

        # Ensure the user does not already have a quote with the same content and author
        if Quote.objects.filter(user=user, content=data.get('content'), author=data.get('author')).exists():
            raise serializers.ValidationError("You already have a quote with this quote and author.")

        return data
    

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'olid', 'created_at', 'cover', 'year', 'edition_key', 'work_key', 'description', 'authors']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'url', 'title', 'description', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
class PinnedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinnedItem
        fields = ['id', 'item_type', 'item_id', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)   
    
class PinnedItemEnrichedSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = PinnedItem
        fields = ["id", "item_type", "item_id", "created_at", "item"]

    def get_item(self, obj):
        model_map = {
            "movie": Movie,
            "series": Series,
            "quote": Quote,
            "link": Link,
            "book": Book,
        }
        serializer_map = {
            "movie": MovieSerializer,
            "series": SeriesSerializer,
            "quote": QuoteSerializer,
            "link": LinkSerializer,
            "book": BookSerializer,
        }

        Model = model_map.get(obj.item_type)
        Ser = serializer_map.get(obj.item_type)
        if not Model or not Ser:
            return None

        try:
            instance = Model.objects.get(id=obj.item_id)
        except Model.DoesNotExist:
            return None
        
        data = Ser(instance, context=self.context).data
        data["type"] = obj.item_type
        return data