import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# take the data from the previous file
df_reviews = pd.read_csv("PSTAT-134-Final/df_reviews.csv")  # Change the file path as needed
### print(df_reviews.head())

# use this data and filter it based on certain speicifcations
df_reviews = df_reviews.dropna(subset=["rating"]) # remove NaN ratings
df_reviews = df_reviews[~df_reviews['review'].str.contains("https://", case=False, na=False)] # reviews like these are just links to other websites
df_reviews = df_reviews[~df_reviews['review'].str.contains("FULL SPOILER-FREE REVIEW", case=False, na=False)] # so are these
df_reviews = df_reviews[~df_reviews['review'].str.contains(r'[^\x00-\x7F]', regex=True, na=False)] # remove non-ASCII character
### print(df_reviews.head(20))
print("DataFrame dimensions:", df_reviews.shape)

# one-hot encode all of the words (tokenization)
df_reviews['tokenized_review'] = df_reviews['review'].astype(str).apply(word_tokenize)
print(df_reviews[['review', 'tokenized_review']].head())

# export this data set for future use






