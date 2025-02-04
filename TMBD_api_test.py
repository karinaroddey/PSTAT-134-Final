import requests

# ---------------------------
# Configuration - Replace these with your actual credentials
# ---------------------------
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3OGJlZDI2ZmZkZTFkNjUyZmY4Mzg1NjY3ZmFkNDNkNSIsIm5iZiI6MTczODY5NDE3Ni4zNDUsInN1YiI6IjY3YTI1ZTIwN2ViYjA2MTRmZjI2YzQ5MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fp7j1XYC78LliyhnWDkAZoH1g8Z5N0CozXTFeuLWIg8"         # Your TMDB API key
SESSION_ID = "YOUR_SESSION_ID"   # The session ID obtained after authenticating the user
ACCOUNT_ID = "YOUR_ACCOUNT_ID"   # The account ID of the authenticated user

# ---------------------------
# 1. Public Endpoints: Reviews and Aggregated Ratings
# ---------------------------

def get_movie_reviews(movie_id, api_key, language="en-US", page=1):
    """
    Fetches reviews for a given movie.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
    params = {
        "api_key": api_key,
        "language": language,
        "page": page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad responses (optional)
    return response.json()

def get_movie_details(movie_id, api_key, language="en-US"):
    """
    Fetches movie details which include aggregated rating data (vote average and vote count).
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key,
        "language": language
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# ---------------------------
# 2. User-Specific Endpoints (Requires Authentication)
# ---------------------------

def get_account_states(movie_id, api_key, session_id):
    """
    Retrieves the account states for a movie. This includes whether the user has rated,
    favorited, or added the movie to their watchlist. The 'rated' field will contain the
    user's rating if they have rated the movie.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/account_states"
    params = {
        "api_key": api_key,
        "session_id": session_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_user_rated_movies(account_id, api_key, session_id, language="en-US", page=1):
    """
    Retrieves a list of all movies that the user has rated.
    """
    url = f"https://api.themoviedb.org/3/account/{account_id}/rated/movies"
    params = {
        "api_key": api_key,
        "session_id": session_id,
        "language": language,
        "page": page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# ---------------------------
# Main Execution
# ---------------------------
if __name__ == "__main__":
    # Example movie_id; you can change this to any valid TMDB movie ID (e.g., 550 for "Fight Club")
    movie_id = 550

    # 1. Get and print movie reviews (public endpoint)
    try:
        reviews_data = get_movie_reviews(movie_id, API_KEY)
        print("=== Movie Reviews ===")
        for review in reviews_data.get("results", []):
            print(f"Author: {review.get('author')}")
            print(f"Content: {review.get('content')}\n{'-'*40}")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching reviews: {http_err}")
    except Exception as err:
        print(f"An error occurred while fetching reviews: {err}")

    # 2. Get and print movie details (includes aggregated ratings)
    try:
        details = get_movie_details(movie_id, API_KEY)
        print("\n=== Movie Details (Aggregated Ratings) ===")
        print(f"Title       : {details.get('title')}")
        print(f"Vote Average: {details.get('vote_average')}")
        print(f"Vote Count  : {details.get('vote_count')}")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching movie details: {http_err}")
    except Exception as err:
        print(f"An error occurred while fetching movie details: {err}")

    # 3. Get and print account states for the movie (user-specific rating, watchlist, favorites)
    try:
        account_states = get_account_states(movie_id, API_KEY, SESSION_ID)
        print("\n=== Account States for the Movie ===")
        # The 'rated' field might be either a boolean or an object containing the rating value.
        rated_info = account_states.get("rated")
        if rated_info:
            if isinstance(rated_info, dict):
                print(f"User's Rating: {rated_info.get('value')}")
            else:
                print("User has rated the movie.")
        else:
            print("User has not rated the movie.")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching account states: {http_err}")
    except Exception as err:
        print(f"An error occurred while fetching account states: {err}")

    # 4. Get and print all movies rated by the authenticated user
    try:
        rated_movies = get_user_rated_movies(ACCOUNT_ID, API_KEY, SESSION_ID)
        print("\n=== Movies Rated by the User ===")
        for movie in rated_movies.get("results", []):
            # Some movies may not have a 'rating' key if the rating is null
            user_rating = movie.get("rating", "Not rated")
            print(f"{movie.get('title')} - User Rating: {user_rating}")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching user's rated movies: {http_err}")
    except Exception as err:
        print(f"An error occurred while fetching user's rated movies: {err}")
