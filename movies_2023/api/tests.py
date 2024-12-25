from rest_framework.test import APITestCase
from rest_framework import status
from .models import *
from .serializers import *

class SerializersTestCases(APITestCase):
    # Set up the movie data
    def setUp(self):
        self.genre = Genre.objects.create(name='Scifi')
        self.director = Director.objects.create(name='Christopher Nolan')
        self.star = Star.objects.create(name='Matthew McConaughey')
        self.movie = Movie.objects.create(title='Interstellar', release_date='2023-11-26', run_time=169, rating=8.7, introduction='When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.')

        # Add the genre, director, and star to the movie
        self.movie.genre.add(self.genre)
        self.movie.director.add(self.director)
        self.movie.stars.add(self.star)

    # Test the Genre serializer
    def testGenreSerializer(self):
        serializer = GenreSerializer(self.genre)
        self.assertEqual(serializer.data, {'id': 1, 'name': 'Scifi'})

    # Test the Director serializer
    def testDirectorSerializer(self):
        serializer = DirectorSerializer(self.director)
        self.assertEqual(serializer.data, {'id': 1, 'name': 'Christopher Nolan'})

    # Test the Star serializer
    def testStarSerializer(self):
        serializer = StarSerializer(self.star)
        self.assertEqual(serializer.data, {'id': 1, 'name': 'Matthew McConaughey'})

    # Test the Movie serializer
    def testMovieSerializer(self):
        serializer = MovieSerializer(self.movie)
        self.assertEqual(serializer.data, {'id': 1, 'title': 'Interstellar', 'release_date': '2023-11-26', 'run_time': 169, 'rating': '8.7', 'introduction': 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.', 'genre': [{'id': 1, 'name': 'Scifi'}], 'director': [{'id': 1, 'name': 'Christopher Nolan'}], 'stars': [{'id': 1, 'name': 'Matthew McConaughey'}]})

class ViewsTestCases(APITestCase):
  
    def setUp(self):
        # Set up the movie data
        self.genre = Genre.objects.create(name='Scifi')
        self.director = Director.objects.create(name='Christopher Nolan')
        self.star = Star.objects.create(name='Matthew McConaughey')
        self.movie = Movie.objects.create(title='Interstellar', release_date='2023-11-26', run_time=169, rating=8.7, introduction='When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.')

        # Add the genre, director, and star to the movie
        self.movie.genre.add(self.genre)
        self.movie.director.add(self.director)
        self.movie.stars.add(self.star)

    # Test getAllMovies() view function
    def testGetAllMovies(self):
        response = self.client.get('/movies/all/')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']) > 0, True)

    # Test getMovieByGenre() view function
    def testGetMovieByGenre(self):
        response = self.client.get('/movies/genres/scifi')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Interstellar')

    # Test getMovieByStarOrDirector() view function
    def testGetMovieByStarOrDirector(self):
        # Test view function by star
        response = self.client.get('/movies/production/?star=Matthew McConaughey')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Interstellar')
        # Test view function by director
        response = self.client.get('/movies/production/?director=Christopher Nolan')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Interstellar')

    # Test searchMovies() view function
    def testSearchMovies(self):
        response = self.client.get('/movies/search/?query=interstellar')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Interstellar')

    # Test deleteMovie() view function
    def testDeleteMovie(self):
        response = self.client.delete('/movies/delete/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(id=self.movie.id).exists())

    # Test updateMovie() view function
    def testUpdateMovie(self):
        response = self.client.put('/movies/update/1/', {'title': 'Interstellar 2'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.get(id=self.movie.id).title, 'Interstellar 2')