import tweepy
import json
import config
import psycopg2
import psycopg2.extras
import time

# Function to connect to database and inserting data in tweets table.
def twitterDB(username, created_time, tweet_id, tweet, place):

    # Connecting to the database.
    connection = psycopg2.connect(host = config.DB_HOST,
                                database = config.DB_NAME,
                                user = config.DB_USER,
                                password = config.DB_PASSWORD)
    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

    # Inserting values in the table.
    cursor.execute("""INSERT INTO tweets (username, created_time, tweet_id, tweet, place)
                        VALUES (%s, %s, %s, %s, %s)""",
                        (username, created_time, tweet_id, tweet, place))
    connection.commit()

""" # Lists to store the data.
username, created_time, tweet_id, tweet, place = ([] for i in range(5)) """

# StreamListener class that inherits StreamListener class in Tweepy library.
class StreamListener(tweepy.StreamListener):

    def __init__(self, api, username, created_time, tweet_id, tweet, place):

        tweepy.StreamListener.__init__(self, api)
        self.username = username
        self.created_time = created_time
        self.tweet_id = tweet_id
        self.tweet = tweet
        self.place = place

    def on_connect(self):    

        print("Connected to Twitter API")

    def on_error(self, status_code):

        if status_code != 200:
            print("Error")
            return False

    # Method to get data from the twitter stream.
    def on_data(self, data):

        raw_data = json.loads(data)
        if 'text' in raw_data:
            self.username = raw_data['user']['screen_name']
            self.created_time = raw_data['created_at']
            self.tweet_id = raw_data['id_str']
            self.tweet = raw_data['text']
            self.place = raw_data['user']['location']

            twitterDB(self.username, self.created_time, self.tweet_id, self.tweet, self.place)

if __name__ == '__main__':

    # Taking the search terms from the user.
    search_words = []
    while True:
        term = input("Enter keyword or enter No to continue : ")
        if term.lower() == 'no' :
            break
        else:
            search_words.append(term)
    
    # Taking the duration of stream from the user.
    while True:
        try:
            duration = int(input("Enter the duration of the stream (in seconds) : "))
            break
        except ValueError :
            print("Enter valid duration.")      


    # Lists to store the data.
    username, created_time, tweet_id, tweet, place = ([] for i in range(5))          

    # Authentication.
    auth = tweepy.OAuthHandler(config.API_key, config.API_secret_key)
    auth.set_access_token(config.Access_token, config.Access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    # Stream.
    tweets_listener = StreamListener(api, username, created_time, tweet_id, tweet, place)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track = search_words, languages = ["en"], is_async = True)
    # Stream disconnection.
    time.sleep(duration)
    stream.disconnect()