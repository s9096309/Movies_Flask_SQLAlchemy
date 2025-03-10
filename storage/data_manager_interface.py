from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def create_user(self, name):
        pass

    @abstractmethod
    def get_movies_by_user(self, user_id):
        pass

    @abstractmethod
    def add_movie(self, user_id, name, director, year, rating):
        pass

    @abstractmethod
    def update_movie(self, movie_id, name, director, year, rating):
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        pass