# SENTIMENT ANALYSIS ON TWITTER STREAMING DATA
***Streaming twitter data and performing sentiment analysis.***

## Project Description
**Aim:** Creating ETL pipeline to stream tweets from twitter and then loading the data in postgres database then performing sentiment analysis on each tweet.
* Database used: PostgreSQL.
* Libraries used: tweepy, psycopg2, nltk, pandas, re and textblob.
* Software used: Docker.
* Languages used: Python and SQL.
* Connection to the postgres database was done using psycopg2.
* Preprocessing on the tweets was done using nltk, pandas and re.
* Analysis was done using textblob.

## How to run
1. Create a twitter developer account and create a project in the dashboard to access your own api keys and tokens.
2. Change the twitter api key, twitter api secret key, access token and access secret token in the **config.py** file.
3. Pull postgres on docker : **docker run --name postgresql -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres**.
4. To go to the postgres terminal : **docker exec -it postgresql bash** then **psql -U postgres**.
5. In the postgres terminal, create a database **twitter** : **CREATE DATABASE twitter;**.
6. Connect to twitter database : **\c twitter**.
7. Create the table required using the query in **tables.sql** file.
8. Run **run.py**.
9. You'll be prompted to enter the keywords and the duration of the stream when you run the program. Enter the values and wait for the analysis report.
