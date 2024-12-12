import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import tweepy
import time

# Twitter API credentials
API_KEY = "ZQsS11xT00W5U9imZFyn02B3z"
API_SECRET = "Z8pPfP03N3JFVhQ8YWFGKF6nM80gWB4tptpZyPTHUiovUBG2rC"
ACCESS_TOKEN = "1132500413058433024-yqTrwEFocCAJLnDiVPqiw5kSlSqtDO8"
ACCESS_TOKEN_SECRET = "l7Hk9WCJ8SvI5xIu1yzbXEVIluj8Wl3hcnvxNLeq7Art6"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAE8IxgEAAAAAvo0XBFE9aAUKlWsoZJtP8FxN0Ak%3DGM6NblKd0zNI4ZY4MQQFKjwumkM5JOT38B7QUMHVODeXWrA0xY"

# Authenticate with Twitter API using the Client class
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Function to fetch tweets with rate limit handling
def fetch_tweets(query, count=10):
    try:
        response = client.search_recent_tweets(query=query, max_results=count, tweet_fields=["lang"])
        tweet_data = [{"Feedback": tweet.text} for tweet in response.data if tweet.lang == "en"]
        return pd.DataFrame(tweet_data)
    except tweepy.errors.TooManyRequests as e:
        print("Rate limit reached. Waiting for 15 minutes...")
        time.sleep(15 * 60)  # Wait for 15 minutes
        return fetch_tweets(query, count)

# Fetch tweets based on a keyword
query = input("Enter a keyword to search tweets: ")
data = fetch_tweets(query, count=5)  # Lowering count to avoid rate limit

# Perform sentiment analysis
def analyze_sentiment(feedback):
    sentiment = TextBlob(feedback).sentiment.polarity
    if sentiment > 0:
        return 'Positive'
    elif sentiment < 0:
        return 'Negative'
    else:
        return 'Neutral'

data['Sentiment'] = data['Feedback'].apply(analyze_sentiment)

# Generate report
summary = data['Sentiment'].value_counts()
print("\nSentiment Summary:")
print(summary)

# Save results to a new file
output_path = "tweets_analysis_output.csv"
data.to_csv(output_path, index=False)
print(f"\nDetailed analysis saved to {output_path}")

# Plotting Sentiment Summary as a Pie Chart
plt.figure(figsize=(6, 6))
summary.plot(kind='pie', autopct='%1.1f%%', startangle=140, labels=summary.index)
plt.title("Sentiment Distribution - Pie Chart")
plt.ylabel('')  # Hides the "Sentiment" label on the y-axis
plt.savefig("tweet_sentiment_pie_chart.png")  # Save the pie chart as an image
plt.show()

# Plotting Sentiment Summary as a Bar Graph
plt.figure(figsize=(8, 6))
summary.plot(kind='bar', color=['green', 'blue', 'red'])
plt.title("Sentiment Distribution - Bar Graph")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("tweet_sentiment_bar_graph.png")  # Save the bar graph as an image
plt.show()
