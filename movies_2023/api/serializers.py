from rest_framework import serializers
from .models import Movie, Genre, Director, Star

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    director = DirectorSerializer(many=True)
    stars = StarSerializer(many=True) 
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'run_time', 'rating', 'introduction', 'genre', 'director', 'stars']