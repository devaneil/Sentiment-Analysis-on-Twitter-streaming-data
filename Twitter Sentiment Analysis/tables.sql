
CREATE TABLE tweets (
    username VARCHAR(50) NOT NULL,
    created_time VARCHAR(100) NOT NULL,
    tweet_id VARCHAR(150) NOT NULL,
    tweet TEXT NOT NULL,    
    place VARCHAR(150),
    PRIMARY KEY (tweet_id)
);