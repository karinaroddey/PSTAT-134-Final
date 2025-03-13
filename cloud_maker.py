import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk import FreqDist
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer

# load data
full_data = pd.read_csv("combined_reviews.csv")
full_data = full_data.dropna(subset=['review_cat'])
#print(full_data.head())

# tokenize all of the words in the reviews
full_data['tokenized_content'] = full_data['content'].apply(lambda x: word_tokenize(str(x)))
full_data = full_data.explode('tokenized_content')

nltk.download('stopwords') # download the stop words ## ONLY NEED TO RUN THIS ONCE
stop_words = set(stopwords.words('english')) # get a premade list of stop words
full_data_filtered = full_data[~full_data['tokenized_content'].isin(stop_words)] # filter out rows with stop words in token columnm
#print(full_data_filtered.head())

# start making some of them word plots
good_reviews = full_data_filtered[full_data_filtered['review_cat'] == 'good'] # filter into good and bad reviews for further analysis
bad_reviews = full_data_filtered[full_data_filtered['review_cat'] == 'bad']

# remove other particular words
words_to_remove = {"movie", "film", "cinema", "s", "n't", "one", ")", "(", ",", "."}
good_reviews = good_reviews[
    ~good_reviews['tokenized_content'].apply(
        lambda tokens: any(word in tokens for word in words_to_remove))]
bad_reviews = bad_reviews[
    ~bad_reviews['tokenized_content'].apply(
        lambda tokens: any(word in tokens for word in words_to_remove))]

# for the good reviews
good_reviews['tokenized_content'] = good_reviews['tokenized_content'].apply(
    lambda x: x if isinstance(x, list) else str(x).split()
)

# drop rows you don't like
good_tokens = good_reviews['tokenized_content'].dropna()

good_string = ' '.join(' '.join(tokens) for tokens in good_tokens) # make the big string
#print(good_string[:500])

# for the bad rows
bad_reviews['tokenized_content'] = bad_reviews['tokenized_content'].apply(
    lambda x: x if isinstance(x, list) else str(x).split()
)

# drop rows you don't like
bad_tokens = bad_reviews['tokenized_content'].dropna()

bad_string = ' '.join(' '.join(tokens) for tokens in bad_tokens) # make the big string
#print(bad_string[:500])

plt.figure(figsize=(12, 6))

# good reviews word cloud
plt.subplot(1, 2, 1)
wordcloud_good = WordCloud(width=400, height=400, background_color='white').generate(good_string)
plt.imshow(wordcloud_good, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud - Good Reviews")

# bad reviews word cloud
plt.subplot(1, 2, 2)
wordcloud_bad = WordCloud(width=400, height=400, background_color='white').generate(bad_string)
plt.imshow(wordcloud_bad, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud - Bad Reviews")

# Display the word clouds
plt.show()