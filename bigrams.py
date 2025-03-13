import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from nltk import FreqDist
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.phrases import Phrases, Phraser
from collections import Counter

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

# this is the bigram section

# make list versions of the the good and bad words
good_tokens_flat = [
    token
    for tokens in good_reviews['tokenized_content'].dropna()
    for token in tokens
]
bad_tokens_flat = [
    token
    for tokens in bad_reviews['tokenized_content'].dropna()
    for token in tokens
]

def token_lists_to_docs(token_lists): # turn the lists into big strings
    return [" ".join(tokens) for tokens in token_lists.dropna()]

good_docs = token_lists_to_docs(good_reviews['tokenized_content'])
bad_docs  = token_lists_to_docs(bad_reviews['tokenized_content'])

# For GOOD reviews
vectorizer_good = CountVectorizer(ngram_range=(2, 2))
X_good = vectorizer_good.fit_transform(good_docs)  # document-term matrix
good_feature_names = vectorizer_good.get_feature_names_out()

# Sum counts across all documents to get global frequency
good_counts = X_good.sum(axis=0).A1  # .A1 flattens to 1D array
good_bigram_freq = list(zip(good_feature_names, good_counts))
# Sort by frequency descending
good_bigram_freq_sorted = sorted(good_bigram_freq, key=lambda x: x[1], reverse=True)

# For BAD reviews
vectorizer_bad = CountVectorizer(ngram_range=(2, 2))
X_bad = vectorizer_bad.fit_transform(bad_docs)
bad_feature_names = vectorizer_bad.get_feature_names_out()

bad_counts = X_bad.sum(axis=0).A1
bad_bigram_freq = list(zip(bad_feature_names, bad_counts))
bad_bigram_freq_sorted = sorted(bad_bigram_freq, key=lambda x: x[1], reverse=True)

def plot_bigram_graph(bigram_list, top_n=10, title="Bigrams Graph"):
    # Slice the top N
    top_bigrams = bigram_list[:top_n]
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add edges for each bigram
    for bigram, freq in top_bigrams:
        w1, w2 = bigram.split(" ", 1)
        G.add_edge(w1, w2, weight=freq)
    
    # Layout for positioning
    # - k: The optimal distance between nodes. Larger k => more spread out nodes.
    # - scale: The overall scale of the layout.
    # - iterations: How many times the layout algorithm iterates.
    # - seed: Makes the layout reproducible.
    pos = nx.spring_layout(G, k=5.0, scale=3.0, iterations=100, seed=3132025)
    
    # Plot
    plt.figure(figsize=(12, 8))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500)
    
    # Draw edges (directed arrows)
    nx.draw_networkx_edges(
        G, pos, 
        arrows=True, 
        arrowstyle="->", 
        connectionstyle="arc3,rad=0.1"
    )
    
    # Draw labels for nodes
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")
    
    # Edge labels for frequencies
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(title)
    plt.axis('off')
    plt.show()
    

# Plot top 10 bigrams for GOOD reviews
plot_bigram_graph(
    bigram_list=good_bigram_freq_sorted,
    top_n=20,
    title="Top 10 Bigrams (Good Reviews)"
)

# Plot top 10 bigrams for BAD reviews
plot_bigram_graph(
    bigram_list=bad_bigram_freq_sorted,
    top_n=20,
    title="Top 10 Bigrams (Bad Reviews)"
)

# pretty much works but could use some tweaking