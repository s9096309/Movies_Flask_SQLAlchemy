import requests
import os
import statistics
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import random
from flask import Flask, url_for
from app import app

load_dotenv()


class MovieApp:
    def __init__(self, data_manager, user_id):
        self._data_manager = data_manager
        self.user_id = user_id
        self.api_key = os.getenv("OMDB_API_KEY")

    def _get_user_movies(self):
        return self._data_manager.get_movies_by_user(self.user_id)

    def _extract_year(self, year_str):
        try:
            return int(year_str.split('–')[0])
        except ValueError:
            print(f"Invalid year format: {year_str}")
            return None

    def _command_list_movies(self):
        movies = self._get_user_movies()
        if not movies:
            print("No movies found.")
            return
        for movie in movies:
            print(f"{movie['title']}: {movie['rating']} ({movie['year']})")

    def _fetch_movie_details(self, title):
        try:
            url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={title}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: Could not connect to OMDb API: {e}")
            return None
        except ValueError as e:
            print(f"Error: Could not decode JSON response: {e}")
            return None

    def _extract_movie_attributes(self, movie_data):
        try:
            movie_title = movie_data['Title']
            year = self._extract_year(movie_data['Year'])
            if year is None:
                return None
            rating = float(movie_data['imdbRating']) if movie_data['imdbRating'] != 'N/A' else 0.0
            poster_url = movie_data['Poster'] if movie_data['Poster'] != 'N/A' else None
            imdb_id = movie_data['imdbID']
            return movie_title, year, rating, poster_url, imdb_id
        except KeyError as e:
            print(f"Error: Missing key in OMDb API response: {e}")
            return None

    def _command_add_movie(self):
        """Adds a movie to the storage using the OMDb API."""
        title = input("Enter the movie title: ")
        if not self.api_key:
            print("Error: OMDB API key is missing!")
            return

        movie_data = self._fetch_movie_details(title)
        if movie_data is None:
            return

        if movie_data['Response'] == 'True':
            movie_attributes = self._extract_movie_attributes(movie_data)
            if movie_attributes is None:
                return

            movie_title, year, rating, poster_url, imdb_id = movie_attributes
            self._data_manager.add_movie(self.user_id, movie_title, movie_data['Director'], year, rating, poster_url,
                                         imdb_id)
            print(f"Movie '{movie_title}' added successfully!")
        else:
            print(f"Error: {movie_data['Error']}")

    def _command_delete_movie(self):
        try:
            movie_id = int(input("Enter movie ID to delete: "))
            self._data_manager.delete_movie(movie_id)
            print(f"Movie deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid movie ID (integer).")

    def _command_movie_stats(self):
        movies = self._get_user_movies()
        if not movies:
            print("No movies to calculate stats.")
            return

        try:
            ratings = [movie['rating'] for movie in movies]
            avg_rating = sum(ratings) / len(ratings)
            median_rating = statistics.median(ratings)
            best_movie = max(movies, key=lambda movie: movie['rating'])
            worst_movie = min(movies, key=lambda movie: movie['rating'])

            print("\nMovie Stats:")
            print(f"  Average rating: {avg_rating:.2f}")
            print(f"  Median rating: {median_rating}")
            print(f"  Best movie: {best_movie['title']}, {best_movie['rating']}")
            print(f"  Worst movie: {worst_movie['title']}, {worst_movie['rating']}")
        except (ValueError, TypeError, statistics.StatisticsError) as e:
            print(f"Error calculating movie stats: {e}")

    def _command_generate_website(self):
        try:
            # Trigger the Flask route for website generation
            response = requests.get(f'http://localhost:5000/generate_website/{self.user_id}')
            print("Website generated succesfully!")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def _command_random_movie(self):
        movies = self._get_user_movies()
        if not movies:
            print("No movies in the database.")
            return

        random_movie = random.choice(movies)
        print(f"Your movie for tonight: {random_movie['title']}, it's rated {random_movie['rating']}")

    def _command_search_movie(self):
        search_term = input("Enter search term: ").lower()
        movies = self._get_user_movies()
        found_movies = [movie for movie in movies if search_term in movie['title'].lower()]
        if found_movies:
            print("Found movies:")
            for movie in found_movies:
                print(f"{movie['title']}: {movie['rating']} ({movie['year']})")
        else:
            print("No movies found.")

    def _command_sort_movies(self):
        movies = self._get_user_movies()
        if not movies:
            print("No movies to sort.")
            return

        try:
            order = input("Sort order (A/D): ").upper()
            if order not in ('A', 'D'):
                print("Invalid order. Using ascending order.")
                order = 'A'

            sorted_movies = sorted(movies, key=lambda movie: movie['rating'], reverse=(order == 'D'))
            print("Sorted movies:")
            for movie in sorted_movies:
                print(f"{movie['title']}: {movie['rating']} ({movie['year']})")
        except (TypeError, KeyError) as e:
            print(f"Error sorting movies: {e}")

    def _command_add_user(self):
        name = input("Enter new username: ")
        if self._data_manager.create_user(name):
            print(f"User '{name}' created successfully.")
        else:
            print(f"Error: User '{name}' already exists.")

    def run(self):
        try:
            while True:
                print("\n*** Movie App Menu ***")
                print("1. List movies")
                print("2. Add movie")
                print("3. Delete movie")
                print("4. Movie stats")
                print("5. Generate website")
                print("6. Random movie")
                print("7. Search movie")
                print("8. Movies sorted by rating")
                print("9. Add user")
                print("0. Exit")

                choice = input("Enter your choice (0-9): ")
                if choice == "1":
                    self._command_list_movies()
                elif choice == "2":
                    self._command_add_movie()
                elif choice == "3":
                    self._command_delete_movie()
                elif choice == "4":
                    self._command_movie_stats()
                elif choice == "5":
                    self._command_generate_website()
                elif choice == "6":
                    self._command_random_movie()
                elif choice == "7":
                    self._command_search_movie()
                elif choice == "8":
                    self._command_sort_movies()
                elif choice == "9":
                    self._command_add_user()
                elif choice == "0":
                    print("Exiting the movie app.")
                    break
                else:
                    print("Invalid choice, please try again.")
        except (ValueError, TypeError) as e:
            print(f"An error occurred: {e}")