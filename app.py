from flask import Flask, render_template, request, redirect, url_for
from storage.sqlite_data_manager import SQLiteDataManager
import os
from jinja2 import Environment, FileSystemLoader
import requests
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
data_manager = SQLiteDataManager(app)

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users_list():
    users = data_manager.get_all_users()
    return render_template('users_list.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        data_manager.create_user(username)
        return redirect(url_for('users_list'))
    return render_template('add_user.html')

@app.route('/generate_website/<int:user_id>')
def generate_website(user_id):
    try:
        movies = data_manager.get_movies_by_user(user_id)

        if not movies:
            return "No movies to display."

        html_content = render_template(
            "index_template.html",
            title="My Movie App", # Add a title
            movie_grid=movies
        )

        # Create index.html within the templates folder
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        index_path = os.path.join(template_dir, 'index.html')

        with open(index_path, "w") as f:
            f.write(html_content)

        return redirect(url_for('index'))  # Redirect to the index route

    except FileNotFoundError:
        return "Error: index_template.html not found."
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_by_id(movie_id)
    if request.method == 'POST':
        name = request.form.get('name', movie.title)
        director = request.form.get('director', movie.director)
        year = int(request.form.get('year', movie.year))
        rating = float(request.form.get('rating', movie.rating))

        data_manager.update_movie(movie_id, name, director, year, rating)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie)

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('index'))  # Redirect to the home page after deletion

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    movies = data_manager.get_movies_by_user(user_id)
    return render_template('user_movies.html', user=user, movies=movies)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.get_user_by_id(user_id)
    if request.method == 'POST':
        # Get the movie title from the form
        title = request.form['name']  # Use 'name' as the field name

        # Fetch movie details from OMDb API
        url = f'http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}'
        response = requests.get(url)
        movie_data = response.json()

        if movie_data.get('Response') == 'True':
            director = movie_data.get('Director')
            year = int(movie_data.get('Year'))
            rating = float(movie_data.get('imdbRating'))
            poster_url = movie_data.get('Poster')
            imdb_id = movie_data.get('imdbID')

            # Add the movie to the database
            data_manager.add_movie(user_id, title, director, year, rating, poster_url, imdb_id)

            return redirect(url_for('user_movies', user_id=user_id))
        else:
            return "Error fetching movie details from OMDb API."

    return render_template('add_movie.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)