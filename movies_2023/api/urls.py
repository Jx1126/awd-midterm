from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/all/', views.getAllMovies, name='get-all-movies'),
    path('movies/genres/', views.getMovieByGenre, name='get-movie-by-genres'),
    path('movies/star/<str:star>/', views.getMovieByStar, name='get-movie-by-star'),
    path('genres/all/', views.getAllGenres, name='get-all-genres'),
]
