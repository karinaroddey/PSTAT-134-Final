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
        movie_title = movie.get("title", "Unknown Title")
        reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
        reviews_params = {"api_key": API_KEY}
        reviews_response = requests.get(reviews_url, params=reviews_params)
        
        if reviews_response.status_code != 200:
            print(f"Error fetching reviews for movie ID {movie_id}: {reviews_response.text}")
            continue

        reviews_data = reviews_response.json()
        movie_reviews = reviews_data.get("results", [])
        for review in movie_reviews:
            # Get the written review content.
            written_review = review.get("content", "")
            # Count the number of words in the review.
            word_count = len(written_review.split())
            # Filter reviews: more than 10 words and fewer than 150 words.
            if word_count > 10 and word_count < 150:
                # Attach the movie_id and movie_title to the review.
                review["movie_id"] = movie_id
                review["movie_title"] = movie_title
                reviews.append(review)
            if len(reviews) >= 500:
                reviews = reviews[:500]  # Trim to exactly 500 if necessary.
                break
        if len(reviews) >= 500:
            break

    movie_page += 1
    if movie_page > movies_data.get("total_pages", 1):
        break

print(f"Collected {len(reviews)} reviews that meet the criteria.")

# Step 3: Put the collected data into a pandas DataFrame.
# Each row contains the movie_id, movie_title, rating (if available), and the written review.
review_data = []
for review in reviews:
    movie_id = review.get("movie_id")
    movie_title = review.get("movie_title")
    # Extract rating from the nested 'author_details'; it may be None.
    rating = review.get("author_details", {}).get("rating")
    written_review = review.get("content")
    review_data.append({
        "movie_id": movie_id,
        "movie_title": movie_title,
        "rating": rating,
        "review": written_review
    })

df_reviews = pd.DataFrame(review_data)
df_reviews = df_reviews.dropna(subset=["rating"])
print(df_reviews.head())

# end of script
