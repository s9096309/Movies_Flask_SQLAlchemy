import os
from flask import Flask, url_for
from storage.sqlite_data_manager import SQLiteDataManager
from movie_app import MovieApp

def main():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
    data_manager = SQLiteDataManager(app)

    with app.app_context():
        while True:
            choice = input("1. Select existing user\n2. Create new user\nEnter your choice: ")
            if choice == '1':
                users = data_manager.get_all_users()
                if not users:
                    print("No users found. Please create a user first.")
                    continue

                print("Available users:")
                for user in users:
                    print(f"{user['id']}. {user['name']}")

                while True:
                    try:
                        user_id = int(input("Select user ID: "))
                        user = data_manager.get_user_by_id(user_id)
                        if user:
                            break
                        else:
                            print("Invalid user ID. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                movie_app = MovieApp(data_manager, user_id)
                movie_app.run()
                break

            elif choice == '2':
                username = input("Enter new username: ")
                if data_manager.create_user(username):
                    print(f"User '{username}' created successfully.")
                else:
                    print(f"Error: User '{username}' already exists.")
            else:
                print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()