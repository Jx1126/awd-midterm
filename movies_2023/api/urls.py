from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.getAllMovies, name='get-all-movies'),
    path('genres/', views.getMovieByGenre, name='get-movie-by-genres'),
    path('production/', views.getMovieByStarOrDirector, name='get-movie-by-star-or-director'),
    path('search/', views.searchMovies, name='search-movies'),
    path('update/', views.updateMovie, name='update-movie'),
]