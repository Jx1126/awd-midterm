from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import pagination
from rest_framework import status
from .models import *
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
def getMovieByGenre(request, genres):
    if not genres:
        return Response({'error': 'No genre provided. Please provide a genre.'}, status=status.HTTP_400_BAD_REQUEST)

    # Split the genres by comma and capitalize the first letter of each genre
    genres = [genre.strip().capitalize() for genre in genres.split(',')]

    # Filter the movies by the genres and prevent duplicate movies
    movies = Movie.objects.filter(genre__name__in=genres).distinct()

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

# POST request to add a new movie
@api_view(['POST'])
def addMovie(request):
    try:
        data = request.data

        # Process genres
        genre_objects = []
        for genre in data.get('genre', []):
            genre_object, _ = Genre.objects.get_or_create(id=genre['id'], defaults={'name': genre['name']})
            genre_objects.append(genre_object.id)

        # Process directors
        director_objects = []
        for director in data.get('director', []):
            director_object, _ = Director.objects.get_or_create(id=director['id'], defaults={'name': director['name']})
            director_objects.append(director_object.id)

        # Process stars
        star_objects = []
        for star in data.get('stars', []):
            star_object, _ = Star.objects.get_or_create(id=star['id'], defaults={'name': star['name']})
            star_objects.append(star_object.id)

        # Create the movie
        movie = Movie.objects.create(title=data['title'], release_date=data.get('release_date'), run_time=data.get('run_time'), rating=data.get('rating'), introduction=data.get('introduction', ''))
        # Add many-to-many relationships
        movie.genre.set(genre_objects)
        movie.director.set(director_objects)
        movie.stars.set(star_objects)

        # Serialize the created movie
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

