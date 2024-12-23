import csv
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_2023.settings')

import django
django.setup()

from api.models import Genre, Director, Star, Movie

csv_path = '../csv/2023_movies.csv'

def loadAndStoreData():
  try:
    with open(csv_path, 'r',encoding='utf-8-sig') as file:
      reader = csv.DictReader(file)

      for row in reader:

        release_date = row['date'] if row['date'] else None
        run_time = row['run_time'] if row['run_time'] else 0
        rating = row['rating'] if row['rating'] else None
        introduction = row['introduction'] if row['introduction'] else 'No Data'

        movie, created = Movie.objects.get_or_create(
        title = row['title'].strip(),
        defaults = {
          'release_date': release_date,
          'run_time': run_time,
          'rating': rating,
          'introduction': introduction
        })

        genres = row['genre'].split(',')
        genre_objects = []
        for genre in genres:
          genre_object, _ = Genre.objects.get_or_create(name=genre.strip())
          genre_objects.append(genre_object)
          movie.genre.set(genre_objects)

        directors = row['director'].split(',')
        director_objects = []
        for director in directors:
          director_object, _ = Director.objects.get_or_create(name=director.strip())
          director_objects.append(director_object)
          movie.director.set(director_objects)

        stars = row['stars'].split(',')
        star_objects = []
        for star in stars:
          star_object, _ = Star.objects.get_or_create(name=star.strip())
          star_objects.append(star_object)
          movie.stars.set(star_objects)

          movie.save()

        print(f'{movie.title} added to the database')
  
  except FileNotFoundError:
    print('File not found')
  except Exception as e:
    print(e)

# Call the function
def main():
  loadAndStoreData()
  print('Data loaded successfully')

main()
