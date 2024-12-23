from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/all/', views.getAllMovies, name='get-all-movies'),
]
