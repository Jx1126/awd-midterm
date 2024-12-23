from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Movie, Genre, Director, Star
from .serializers import MovieSerializer, GenreSerializer, DirectorSerializer, StarSerializer

@api_view(['GET'])
def getAllMovies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
