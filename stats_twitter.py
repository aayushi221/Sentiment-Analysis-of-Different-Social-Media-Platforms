# -*- coding: utf-8 -*-
"""Stats_Twitter.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EfjcbAYLF-NPbo8JAtyeYo93DzI93aap
"""

!pip install pandas nltk textblob matplotlib seaborn

import pandas as pd
import numpy as np
import nltk
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import re


nltk.download('stopwords')
from nltk.corpus import stopwords

# Load the dataset
df = pd.read_csv('/content/drive/MyDrive/Stats_EAS508/Tweets.csv')
# Display the first few rows
df.head()

print(df.columns)

# Check the size of the dataset
dataset_size = df.shape
print(f"The dataset has {dataset_size[0]} rows and {dataset_size[1]} columns.")

# Remove duplicates and null values
df.drop_duplicates(inplace=True)
df.dropna(subset=['text'], inplace=True)

# Text preprocessing function
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user mentions
    text = re.sub(r'@\w+', '', text)
    # Remove special characters and numbers
    text = re.sub(r'\d+|[^\w\s]', '', text)
    # Remove stopwords
    words = [word for word in text.split() if word not in stop_words]
    return " ".join(words)

# Apply preprocessing
df['cleaned_comment'] = df['text'].apply(preprocess_text)

# Sentiment analysis function
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Apply sentiment analysis
df['sentiment_score'] = df['cleaned_comment'].apply(get_sentiment)

# Categorize sentiment
df['sentiment'] = df['sentiment_score'].apply(lambda score: 'positive' if score > 0 else ('negative' if score < 0 else 'neutral'))

# Display processed data
df[['text', 'cleaned_comment', 'sentiment_score', 'sentiment']].head()

def get_sentiment_score(text):
    # Use TextBlob to calculate sentiment polarity (-1 to 1)
    return TextBlob(text).sentiment.polarity

# Apply the function to the 'text' column to get sentiment scores
df['sentiment_score'] = df['text'].apply(get_sentiment_score)

# Show the dataset with sentiment scores
print(df)

import matplotlib.pyplot as plt
import seaborn as sns

# Plot the sentiment scores distribution
plt.figure(figsize=(8, 6))
sns.histplot(df['sentiment_score'], bins=20, kde=True, color='skyblue', edgecolor='black')

# Adding labels and title
plt.title('Distribution of Sentiment Scores', fontsize=16)
plt.xlabel('Sentiment Score', fontsize=14)
plt.ylabel('Frequency', fontsize=14)

# Show the plot
plt.show()

# Plotting the distribution of sentiments
sns.countplot(x='sentiment', data=df, palette='viridis')
plt.title("Sentiment Distribution")
plt.show()

from wordcloud import WordCloud

# Word cloud for positive comments
positive_comments = " ".join(df[df['sentiment'] == 'positive']['cleaned_comment'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_comments)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud for Positive Comments")
plt.show()