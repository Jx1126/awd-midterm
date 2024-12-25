import csv
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_2023.settings')

import django
django.setup()

from api.models import Genre, Director, Star, Movie

csv_path = '../csv/2023_movies.csv'

def loadAndStoreData():
    try:
        # Open the CSV file and read the data
        with open(csv_path, 'r',encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            print('Loading data...')

            for row in reader:
                # Get the movie data from the CSV file and set the default values if the data is not available
                release_date = row['date'] if row['date'] else None
                run_time = row['run_time'] if row['run_time'] else 0
                rating = row['rating'] if row['rating'] else None
                introduction = row['introduction'] if row['introduction'] else 'No Data'

                # Create a new movie object
                movie, created = Movie.objects.get_or_create(
                    # Get the title and remove whitespaces
                    title = row['title'].strip(),
                    # Set the default values for the movie object
                    defaults = {'release_date': release_date, 'run_time': run_time, 'rating': rating, 'introduction': introduction}
                )

                # Get the genres and split them by comma
                genres = row['genre'].split(',')
                genre_objects = []
                for genre in genres:
                    # Get or create the genre object depending on whether it exists or not
                    genre_object, _ = Genre.objects.get_or_create(name=genre.strip())
                    # Add the genre object to the genre_objects
                    genre_objects.append(genre_object)
                # Set the genres for the movie
                movie.genre.set(genre_objects)

                # Get the directors and split them by comma
                directors = row['director'].split(',')
                director_objects = []
                for director in directors:
                    # Get or create the director object depending on whether it exists or not
                    director_object, _ = Director.objects.get_or_create(name=director.strip())
                    # Add the director object to the director_objects
                    director_objects.append(director_object)
                # Set the directors for the movie
                movie.director.set(director_objects)

                stars = row['stars'].split(',')
                star_objects = []
                for star in stars:
                    # Get or create the star object depending on whether it exists or not
                    star_object, _ = Star.objects.get_or_create(name=star.strip())
                    # Add the star object to the star_objects
                    star_objects.append(star_object)
                # Set the stars for the movie
                movie.stars.set(star_objects)

                # Save the movie object
                movie.save()

    # Return error messages
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(e)

# Call the function
def main():
    loadAndStoreData()
    print('Data loaded successfully')

main()
