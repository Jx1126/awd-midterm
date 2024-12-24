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

# GET request to return movies by genre
@api_view(['GET'])
def getMovieByGenre(request):
    # Get the genres from the query parameters
    genres = request.query_params.getlist('genre')
    # Capitalize the firt letter of the genre to match the database
    genres = [genre.capitalize() for genre in genres]

    movies = Movie.objects.filter(genre__name__in=genres)
    # Serialize the data and return the response
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# GET request to return movies by director or star
@api_view(['GET'])
def getMovieByStarOrDirector(request):
    # Get the star or director from the query parameters
    star = request.query_params.get('star')
    director = request.query_params.get('director')
    movies = Movie.objects.all()

    # Filter the movies by the star
    if star:
        movies = Movie.objects.filter(stars__name__iexact=star)
    # Filter the movies by the director
    if director:
        movies = Movie.objects.filter(director__name__iexact=director)

    # Serialize the data and return the response
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# GET request to return all genres
@api_view(['GET'])
def getAllGenres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)