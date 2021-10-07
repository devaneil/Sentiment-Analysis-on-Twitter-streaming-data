import psycopg2
import psycopg2.extras
import config
import pandas as pd
import re
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class SentimentAnalysis():
    
    def __init__(self, host, database, user, password):

        self.host = host
        self.database = database
        self.user = user
        self.password = password

    # Method to connect to the database and extract data with SQL query.
    def dbconnect(self, query):

        connection = psycopg2.connect(host = self.host,
                                        database = self.database,
                                        user = self.user,
                                        password = self.password)
        cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data = data,
                            columns = ['username','created_time','tweet_id', 'tweet', ' place'])
        df.to_csv('data.csv')
        return df

    # Method to perform preprocessing before sentiment analysis.
    def preprocess(self, df):

        cleantweets = [] # New list to store the cleaned tweets.
        stem = PorterStemmer()

        for i in range(df.shape[0]):  

            tweet = df['tweet'][i].lower() # Making the words in the tweet to lower case.
            tweet = re.sub(r'[^\w\s]',"", tweet) # Removing special characters.
            words = word_tokenize(tweet) # Tokenizing the words in the tweet.
            words = [word for word in words if not word in stopwords.words('english')] # Removing stop words.
            words = [stem.stem(word) for word in words] # Stemming to root word.
            cleantweets.append(' '.join(words)) # Joining all the words in the words list.

        return cleantweets

    # Method to perform sentiment analysis using TextBlob.
    def analysis(self, tweet):

        analysis = TextBlob(tweet)

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment == 0:
            return 0
        else:
            return -1

if __name__ == '__main__':

    sentiment = SentimentAnalysis(config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD) # Class instantiation.
    data = sentiment.dbconnect(""" SELECT * FROM tweets """) # Calling the dbconnect method.
    cleantweets = sentiment.preprocess(data) # Calling the preprocess method.
    # Creating a new column Sentiment which will store the sentiment of the tweet and saving the new data as csv.
    data['Sentiment'] = [sentiment.analysis(i) for i in cleantweets] 
    data.to_csv('analysis.csv')

    # Number of positive, negative and neutral tweets.
    positive = len(data[data['Sentiment'] == 1]['Sentiment'])
    negative = len(data[data['Sentiment'] == -1]['Sentiment'])
    neutral = len(data[data['Sentiment'] == 0]['Sentiment'])

    # Printing the result.
    print('----------------------------------------')
    print("Number of positive tweets : {}".format(positive))
    print("Number of negative tweets : {}".format(negative))
    print("Number of neutral tweets : {}".format(neutral))
    print("Percentage of positive tweets : {}".format(round((positive/data.shape[0])*100,2)))
    print("Percentage of negative tweets : {}".format(round((negative/data.shape[0])*100,2)))
    print("Percentage of neutral tweets : {}".format(round((neutral/data.shape[0])*100,2)))
    print('----------------------------------------')