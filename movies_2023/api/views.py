from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import pagination
from rest_framework import status
from .models import Movie, Genre, Director, Star
from .serializers import MovieSerializer, GenreSerializer, DirectorSerializer, StarSerializer

# GET request to return all movies in certain order
@api_view(['GET'])
def getAllMovies(request):
    # Get the order from the query parameters
    order = request.query_params.get('order')
    movies = Movie.objects.all()

    # Order the movies based on the query parameters
    if order == 'title_asc':
        movies = movies.order_by('title')
    elif order == 'title_desc':
        movies = movies.order_by('-title')
    elif order == 'release_asc':
        movies = movies.order_by('release_date')
    elif order == 'release_desc':
        movies = movies.order_by('-release_date')
    elif order == 'rating_asc':
        movies = movies.order_by('rating')
    elif order == 'rating_desc':
        movies = movies.order_by('-rating')
    elif order == 'runtime_asc':
        movies = movies.order_by('runtime')
    elif order == 'runtime_desc':
        movies = movies.order_by('-runtime')
    elif order == 'id_desc':
        movies = movies.order_by('-id')
    else:
        movies = movies.order_by('id')

    # Paginate the movies
    paginator = pagination.DataPagination()
    paginated_movies = paginator.paginate_queryset(movies, request)

    # Serialize the data and return the response
    serializer = MovieSerializer(paginated_movies, many=True)
    return paginator.get_paginated_response(serializer.data)

# GET request to return movies by genre
@api_view(['GET'])
def getMovieByGenre(request):
    # Get the genres from the query parameters
    genres = request.query_params.getlist('genre')
    # Capitalize the firt letter of the genre to match the database
    genres = [genre.capitalize() for genre in genres]

    # Filter the movies by the genre
    movies = Movie.objects.filter(genre__name__in=genres)

    # Paginate the movies
    paginator = pagination.DataPagination()
    paginated_movies = paginator.paginate_queryset(movies, request)

    # Serialize the data and return the response
    serializer = MovieSerializer(paginated_movies, many=True)
    return paginator.get_paginated_response(serializer.data)

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

    # Paginate the movies
    paginator = pagination.DataPagination()
    paginated_movies = paginator.paginate_queryset(movies, request)

    # Serialize the data and return the response
    serializer = MovieSerializer(movies, many=True)
    return paginator.get_paginated_response(serializer.data)

# GET request to search for movies by title
@api_view(['GET'])
def searchMovies(request):
    # Get the search query from the query parameters
    query = request.query_params.get('query')
    # Filter the movies by the search query
    movies = Movie.objects.filter(title__icontains=query)

    # Paginate the movies
    paginator = pagination.DataPagination()
    paginated_movies = paginator.paginate_queryset(movies, request)

    # Serialize the data and return the response
    serializer = MovieSerializer(paginated_movies, many=True)
    return paginator.get_paginated_response(serializer.data)
    
# PUT request to update a movie data
@api_view(['PUT'])
def updateMovie(request):
    # Get the movie by the id
    movie = Movie.objects.get(id=request.data['id'])
    # Serialize the request data
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    if serializer.is_valid():
        # Save the updated movie data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)