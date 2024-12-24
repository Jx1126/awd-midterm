from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/all/', views.getAllMovies, name='get-all-movies'),
    path('movies/genre/<str:genre>/', views.getMovieByGenre, name='get-movie-by-genre'),
    path('movies/star/<str:star>/', views.getMovieByStar, name='get-movie-by-star'),
    path('genres/all/', views.getAllGenres, name='get-all-genres'),
]
