from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.getAllMovies, name='get-all-movies'),
    path('genres/', views.getMovieByGenre, name='get-movie-by-genres'),
    path('production/', views.getMovieByStarOrDirector, name='get-movie-by-star-or-director'),
    path('genres/all/', views.getAllGenres, name='get-all-genres'),
]
