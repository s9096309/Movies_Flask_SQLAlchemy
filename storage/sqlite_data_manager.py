import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from storage.data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = SQLAlchemy(app)

        class User(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            name = self.db.Column(self.db.String(80), unique=True, nullable=False)
            movies = self.db.relationship('Movie', backref='user', lazy=True)

        class Movie(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            title = self.db.Column(self.db.String(120), nullable=False)
            director = self.db.Column(self.db.String(120))
            year = self.db.Column(self.db.Integer)
            rating = self.db.Column(self.db.Float)
            poster_url = self.db.Column(self.db.String(255))
            imdb_id = self.db.Column(self.db.String(20))
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('user.id'), nullable=False)

        self.User = User
        self.Movie = Movie
        with app.app_context():
            self.db.create_all()

    def _convert_to_dict(self, db_object):
        return {col.name: getattr(db_object, col.name) for col in db_object.__table__.columns}

    def get_all_users(self):
        users = self.User.query.all()
        return [self._convert_to_dict(user) for user in users]

    def get_user_by_id(self, user_id):
        user = self.User.query.get(user_id)
        if user:
            return self._convert_to_dict(user)
        return None

    def create_user(self, name):
        try:
            new_user = self.User(name=name)
            self.db.session.add(new_user)
            self.db.session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:  # Catch IntegrityError for duplicate user names
            self.db.session.rollback()
            return False

    def add_movie(self, user_id, title, director, year, rating, poster_url, imdb_id):
        try:
            new_movie = self.Movie(user_id=user_id, title=title, director=director, year=year, rating=rating,
                                   poster_url=poster_url, imdb_id=imdb_id)
            self.db.session.add(new_movie)
            self.db.session.commit()
        except Exception as e:  # Catch any database error
            self.db.session.rollback()
            print(f"Database error: {e}")

    def get_movies_by_user(self, user_id):
        movies = self.Movie.query.filter_by(user_id=user_id).all()
        return [self._convert_to_dict(movie) for movie in movies]

    def update_movie(self, movie_id, name, director, year, rating):
        movie = self.Movie.query.get(movie_id)
        if movie:
            movie.name = name
            movie.director = director
            movie.year = year
            movie.rating = rating
            self.db.session.commit()

    def delete_movie(self, movie_id):
        movie = self.Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()

    def get_movie_by_id(self, movie_id):
        movie = self.Movie.query.get(movie_id)
        return movie