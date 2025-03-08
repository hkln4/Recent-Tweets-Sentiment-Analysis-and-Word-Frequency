import requests
import csv
from collections import Counter
import re
from textblob import TextBlob
from requests.structures import CaseInsensitiveDict

with open("bearertoken.txt", mode="r") as file:
    bearer_token = file.read().strip()

# Twitter API access
url = "https://api.twitter.com/2/tweets/search/recent"
headers = CaseInsensitiveDict()
headers["Authorization"] = f"Bearer {bearer_token}"

params = {
    "query": "Oscars2025 lang:en",  # the words you want to search
    "max_results": 40,  # tweet limit
    "tweet.fields": "created_at,author_id"  # Bu alanları API yanıtına dahil et
}

# API request
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print("Request successful!")
    tweets_data = response.json()  # get the response as JSON

    # save the tweets to a CSV file
    with open("tweets.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Tweet", "Created At", "Author ID", "Sentiment"])

        words = []

        for tweet in tweets_data.get('data', []):
            tweet_text = tweet.get('text', 'N/A')
            tweet_created_at = tweet.get('created_at', 'N/A')
            tweet_author_id = tweet.get('author_id', 'N/A')

            # sentiment analysis
            blob = TextBlob(tweet_text)
            sentiment = blob.sentiment.polarity

            # word frequency analysis
            words.extend(re.findall(r'\w+', tweet_text.lower()))

            # write to CSV
            writer.writerow([tweet_text, tweet_created_at, tweet_author_id, sentiment])

    # word frequency analysis
    word_counts = Counter(words)

    # Write most common words to a text file
    with open("common_words.txt", mode="w", encoding="utf-8") as txt_file:
        txt_file.write("Most common words:\n")
        for word, count in word_counts.most_common(10):
            txt_file.write(f"{word}: {count}\n")

    print("Most common words saved to 'common_words.txt'!")

else:
    print(f"Failed to retrieve tweets. Status code: {response.status_code}")
