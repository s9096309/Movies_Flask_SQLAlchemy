# Movie App

This application allows you to manage your movie collection through both a command-line interface and a web interface built with Flask.

## Features

### Command-Line Interface
* Add movies to your collection by searching for them online using the OMDb API.
* View details of movies in your collection, including title, year, rating, and poster.
* Generate a website to showcase your movie collection.
* View statistics about your movie collection, such as average rating and best/worst movies.
* Sort movies by rating.
* Search for movies by title.
* Get a random movie suggestion.
* Add new users to the application.

### Web Interface
* View a list of all users.
* View details of a user's movie collection.
* Add new users.
* Add movies to a user's collection.
* Update existing movie details.
* Delete movies from a user's collection.

## Installation

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd movie-app`
3. Install the required packages: `pip install -r requirements.txt`
4. Create a `.env` file in the project directory and add your OMDb API key:
OMDB_API_KEY=your_omdb_api_key

## Usage

### Command-Line Interface
1. Run the application: `python main.py`
2. Follow the on-screen menu to interact with the application.

### Web Interface
1. Run the Flask application: `python app.py`
2. Access the web interface in your browser at `http://127.0.0.1:5000/`

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.