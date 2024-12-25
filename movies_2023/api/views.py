from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import pagination
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer

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

    # Return an error if no movies are found
    if not movies.exists():
        return Response({'error': 'No movies found.'}, status=status.HTTP_404_NOT_FOUND)

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

    # Return an error if no genres are provided in the query parameters
    if not genres:
        return Response({'error': 'No genres provided. Please provide at least one genre.'}, status=status.HTTP_400_BAD_REQUEST)

    # Capitalize the firt letter of the genre to match the database
    genres = [genre.capitalize() for genre in genres]

    # Filter the movies by the genre
    movies = Movie.objects.filter(genre__name__in=genres)

    # Return an error if no movies are found for the genres
    if not movies.exists():
        return Response({'error': 'No movies found for the provided genres.'}, status=status.HTTP_404_NOT_FOUND)

    # Paginate the movies
    paginator = pagination.DataPagination()
    paginated_movies = paginator.paginate_queryset(movies.order_by('id'), request)

    # Serialize the data and return the response
    serializer = MovieSerializer(paginated_movies, many=True)
    return paginator.get_paginated_response(serializer.data)

# GET request to return movies by director or star
@api_view(['GET'])
def getMovieByStarOrDirector(request):
    # Get the star or director from the query parameters
    star = request.query_params.get('star')
    director = request.query_params.get('director')

    # Return an error if no star and director are provided in the query parameters
    if not star and not director:
        return Response({'error': 'Please provide a star or director name.'}, status=status.HTTP_400_BAD_REQUEST)

    movies = Movie.objects.all()

    # Filter the movies by the star
    if star:
        movies = Movie.objects.filter(stars__name__iexact=star)
    # Filter the movies by the director
    if director:
        movies = Movie.objects.filter(director__name__iexact=director)

    # Return an error if no movies are found for the star or director
    if not movies.exists():
        return Response({'error': 'No movies found for the provided star or director.'}, status=status.HTTP_404_NOT_FOUND)

    # Paginate the movies
    paginator = pagination.DataPagination()
    paginated_movies = paginator.paginate_queryset(movies.order_by('id'), request)

    # Serialize the data and return the response
    serializer = MovieSerializer(paginated_movies, many=True)
    return paginator.get_paginated_response(serializer.data)

# GET request to search for movies by title
@api_view(['GET'])
def searchMovies(request):
    # Get the search query from the query parameters
    query = request.query_params.get('query')

    # Return an error if no search query is provided
    if not query:
        return Response({'error': 'Please provide a search query.'}, status=status.HTTP_400_BAD_REQUEST)

    # Filter the movies by the search query
    movies = Movie.objects.filter(title__icontains=query)

    # Return an error if no movies are found for the search query
    if not movies.exists():
        return Response({'error': 'No movies found for the provided search query.'}, status=status.HTTP_404_NOT_FOUND)

    # Paginate the movies
    paginator = pagination.DataPagination()
    paginated_movies = paginator.paginate_queryset(movies.order_by('id'), request)

    # Serialize the data and return the response
    serializer = MovieSerializer(paginated_movies, many=True)
    return paginator.get_paginated_response(serializer.data)

# DELETE request to delete a movie
@api_view(['DELETE'])
def deleteMovie(request, movie_id):
    try:
        # Get the movie by the id
        movie = Movie.objects.get(id=movie_id)
        # Delete the movie
        movie.delete()
        return Response("message: Movie deleted successfully", status=status.HTTP_204_NO_CONTENT)
    # Return an error if the movie does not exist
    except Movie.DoesNotExist:
        return Response({'error': 'Movie does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
# PUT request to update a movie data
@api_view(['PUT'])
def updateMovie(request, movie_id):
    try:
        # Get the movie by the id
        movie = Movie.objects.get(id=movie_id)
    # Return an error if the movie does not exist
    except Movie.DoesNotExist:
        return Response({'error': 'Movie does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Serialize the request data and allow partial updates
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    if serializer.is_valid():
        # Save the updated movie data if it is valid
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)