import pandas as pd
import nltk
import re
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV

# Download necessary NLTK data files
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the dataset
full_data = pd.read_csv("combined_reviews.csv")

# Preprocessing function
def preprocess_text(text):
    text = text.lower()  # Lowercase conversion
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    text = " ".join([lemmatizer.lemmatize(word) for word in words if word not in stop_words])
    return text

# Apply text preprocessing
full_data['clean_content'] = full_data['content'].astype(str).apply(preprocess_text)

# Sentiment labeling
full_data['sentiment'] = full_data['rating'].apply(lambda x: 1 if x >= 8 else (-1 if x <= 4 else 0))

# Initialize TF-IDF Vectorizer with n-grams
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2), max_df=0.9, min_df=5)
X = vectorizer.fit_transform(full_data['clean_content']).toarray()
y = full_data['sentiment']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3132025)

# Initialize and optimize Logistic Regression
log_reg = LogisticRegression(solver='liblinear', class_weight='balanced')
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)

# Evaluate Logistic Regression Model
print("Logistic Regression Performance:")
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(f'Classification Report:\n {classification_report(y_test, y_pred)}')

# Confusion Matrix
plt.figure(figsize=(5,4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=[-1,0,1], yticklabels=[-1,0,1])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Logistic Regression")
plt.show()

# Alternative Model: Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("Random Forest Performance:")
print(f'Accuracy: {accuracy_score(y_test, y_pred_rf)}')
print(f'Classification Report:\n {classification_report(y_test, y_pred_rf)}')

# Hyperparameter Tuning for Logistic Regression
param_grid = {'C': [0.01, 0.1, 1, 10]}
grid_search = GridSearchCV(LogisticRegression(solver='liblinear', class_weight='balanced'), param_grid, cv=5)
grid_search.fit(X_train, y_train)
print(f'Best Logistic Regression Hyperparameters: {grid_search.best_params_}')

# Function to Predict Sentiment
def predict_sentiment(review):
    review_cleaned = preprocess_text(review)
    review_tfidf = vectorizer.transform([review_cleaned]).toarray()
    sentiment = log_reg.predict(review_tfidf)[0]
    return "Positive" if sentiment == 1 else "Negative" if sentiment == -1 else "Neutral"

# Example Prediction
new_review = "Heretic was pretty boring and my friend hyped it up too much"
print(f'Review: {new_review}')
print(f'Sentiment: {predict_sentiment(new_review)}')

# Plot Sentiment Distribution
full_data['sentiment'].value_counts().plot(kind='bar', color=['green', 'blue', 'red'])
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()
