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

for movie_id in range(5000, 10001):
    # First, fetch movie details to obtain the movie title.
    movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    details_params = {"api_key": API_KEY}
    details_response = requests.get(movie_details_url, params=details_params)
    
    if details_response.status_code != 200:
        # Movie not found or other error; skip to the next movie_id.
        continue
    
    movie_details = details_response.json()
    movie_title = movie_details.get("title", "Unknown Title")
    
    # Now, fetch reviews for the movie.
    reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
    reviews_params = {"api_key": API_KEY}
    reviews_response = requests.get(reviews_url, params=reviews_params)
    
    if reviews_response.status_code != 200:
        # Unable to fetch reviews; skip this movie.
        continue
    
    reviews_data = reviews_response.json()
    movie_reviews = reviews_data.get("results", [])
    
    # Process each review and filter by word count.
    for review in movie_reviews:
        written_review = review.get("content", "")
        word_count = len(written_review.split())
        if word_count > 10 and word_count < 150:
            review["movie_id"] = movie_id
            review["movie_title"] = movie_title
            reviews.append(review)

print(f"Collected {len(reviews)} reviews from movies with IDs in the range 5000–10001.")

# Step 3: Build the pandas DataFrame.
review_data = []
for review in reviews:
    movie_id = review.get("movie_id")
    movie_title = review.get("movie_title")
    rating = review.get("author_details", {}).get("rating")
    written_review = review.get("content")
    review_data.append({
        "movie_id": movie_id,
        "movie_title": movie_title,
        "rating": rating,
        "review": written_review
    })

df_reviews = pd.DataFrame(review_data)
print("DataFrame with reviews:")
print(df_reviews.head())

df_reviews.to_csv("PSTAT-134-Final/df_reviews.csv", index=False)
print("DataFrame saved as 'df_reviews.csv' in the current directory.")

# end of script
