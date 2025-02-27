import requests
import json
import numpy as np
import pandas as pd

# generate a session token
API_KEY = "78bed26ffde1d652ff8385667fad43d5"
url = "https://api.themoviedb.org/3/authentication/guest_session/new"

params = {
    "api_key": API_KEY
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    guest_session_id = data.get("guest_session_id")
    print("Guest Session ID:", guest_session_id)
else:
    print("Error creating session:", response.text)

# use the API to get a list of movies and their reviews
reviews = []
movie_page = 1

while len(reviews) < 500:
    # Fetch a page of popular movies.
    movies_url = "https://api.themoviedb.org/3/movie/popular"
    movies_params = {
        "api_key": API_KEY,
        "page": movie_page
    }
    movies_response = requests.get(movies_url, params=movies_params)
    
    if movies_response.status_code != 200:
        print("Error fetching popular movies:", movies_response.text)
        break

    movies_data = movies_response.json()
    movie_results = movies_data.get("results", [])
    if not movie_results:
        # No more movies to process.
        break

    # For each movie, get its reviews.
    for movie in movie_results:
        movie_id = movie["id"]
        reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
        reviews_params = {"api_key": API_KEY}
        reviews_response = requests.get(reviews_url, params=reviews_params)
        
        if reviews_response.status_code != 200:
            print(f"Error fetching reviews for movie ID {movie_id}: {reviews_response.text}")
            continue

        reviews_data = reviews_response.json()
        movie_reviews = reviews_data.get("results", [])
        reviews.extend(movie_reviews)

        # Stop if we have reached (or exceeded) 500 reviews.
        if len(reviews) >= 500:
            reviews = reviews[:500]  # Trim to exactly 500 if needed.
            break

    # Prepare to fetch the next page of movies.
    movie_page += 1
    # If we've gone past the total available pages, exit the loop.
    if movie_page > movies_data.get("total_pages", 1):
        break

print(f"Collected {len(reviews)} reviews")
# Optionally, process the reviews as needed

# compile this list into a format easily usable for machine learning models to train on
review_data = []
for review in reviews:
    movie_id = review.get('movie_id')
    # The rating is nested inside the 'author_details' key (it might be None)
    rating = review.get('author_details', {}).get('rating')
    written_review = review.get('content')
    
    review_data.append({
        'movie_id': movie_id,
        'rating': rating,
        'review': written_review
    })

# Create a DataFrame with the extracted data.
df_reviews = pd.DataFrame(review_data)

# Display the first few rows of the DataFrame.
print(df_reviews.head())

# end of script
