import requests
import json

url = "https://api.themoviedb.org/3/movie/78/reviews?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Yjk1ZmYzYjI1NGIwNzZhYzJjZTMxMTMxOTM0NzQ1NSIsIm5iZiI6MTczODYyNjEzNS4xNjgsInN1YiI6IjY3YTE1NDU3MzVkMzA5NzViNjAyZjNjMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RWuafLSvt3cB6r8s2kK6HxH5pNy4kBUD8e9-64iPfS4"
}

response = requests.get(url, headers=headers)
data = response.json()

# Extracted Reviews
reviews = data.get("results", [])

# Categorized Data
review_categories = {
    "Author_Info": [],
    "Ratings": [],
    "Review_Content": [],
    "Review_Metadata": []
}

for review in reviews:
    author_details = review.get("author_details", {})
    
    review_categories["Author_Info"].append({
        "Author": review.get("author", "Unknown"),
        "Username": author_details.get("username", "Unknown"),
        "Avatar Path": author_details.get("avatar_path", "None")
    })
    
    review_categories["Ratings"].append({
        "Author": review.get("author", "Unknown"),
        "Rating": author_details.get("rating", "No Rating")
    })
    
    review_categories["Review_Content"].append({
        "Author": review.get("author", "Unknown"),
        "Review": review.get("content", "No Content")
    })
    
    review_categories["Review_Metadata"].append({
        "Author": review.get("author", "Unknown"),
        "Created At": review.get("created_at", "Unknown"),
        "Updated At": review.get("updated_at", "Unknown"),
        "Review URL": review.get("url", "Unknown")
    })

# Print results in structured format
print(json.dumps(review_categories, indent=4))
