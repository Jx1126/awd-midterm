from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.getAllMovies, name='get-all-movies'),
    path('genres/<str:genres>/', views.getMovieByGenre, name='get-movie-by-genres'),
    path('production/', views.getMovieByStarOrDirector, name='get-movie-by-star-or-director'),
    path('search/', views.searchMovies, name='search-movies'),
    path('delete/<int:movie_id>/', views.deleteMovie, name='delete-movie'),
    path('add/', views.addMovie, name='add-movie'),
]