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

@api_view(['GET'])
def getMovieByGenre(request, genre):
    genre = Genre.objects.get(name=genre)
    movies = genre.movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMovieByStar(request, star):
    star = Star.objects.get(name=star)
    movies = star.movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllGenres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)