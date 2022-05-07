# Avneet Chhabra, akc7yr@virginia.edu
import tweepy
import json 
import requests
import logging
import time


# This is the code for a twitter bot that responds to tweets asking for a quote with an inspirational one from an online API.
# ACCOUNT HANDLE: @avneetquotes !!!!!!!
# One shortcoming I will acknowledge is that it does not respond to DMs, rather, it responds to public tweets requesting quotes or support. Upon further research, I believe there is an issue with tweepy and twitter in terms of having access to the endpoint used to respond to DMs, or at least there was this issue with the version I had downloaded to complete this project. Additionally, a developer community post I found from February 2022 included a statement from someone within Twitter noting this issue. Regardless, it meets all other project benchmarks. 
# 1. Your bot should reply promptly with an intelligent response or an informative error
# message --> Responds to tweets with quotes or requests 
# 2. Your bot should recognize a "help" or "info" message and return user instructions --> Encourages DMing for more information 
# 3. Your bot should integrate with at least one external data source that you can document
# and
# describe. This could be a database system or API. --> Connected to quotable API 

consumer_key = "muEQlDxv442DY1NkBCcprAIxY"
consumer_secret ="EcKv175h7CVQ63jxG0zgyxZXIV6q1dtWKK5UXbfzZmT9I2dXTX"
access_token = "1521987317509943296-D4p65k93A9vN60Mjbjm7qQdOm8YtIA"
access_token_secret ="yrb2FXQDmLgjjyGcOSkVmJETWrm2do34Ab9FCvq2XBqpe"


#pulls random quote from quotable API
def get_quote():
    URL = "https://api.quotable.io/random"
    try:
        response = requests.get(URL)
    except:
        print("Error while calling API...")
    res = json.loads(response.text)
    return res['content'] + "-" + res['author']

#connects to API
def create_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
    except Exception as e:
        logging.error("Error creating API", exc_info=True)
        raise e
    logging.info("API created")
    return api

#checks mentions for quote requests or support requests 
def check_mentions(api, keywords, since_id):
    logging.info("Retrieving mentions")
    new_since_id = since_id
    for status in tweepy.Cursor(api.user_timeline).items():
      try:
        api.destroy_status(status.id)
      except:
        pass
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logging.info(f"Answering to {tweet.user.name}")
            api.update_status(
                status="Feel free to DM for more information about this bot!", in_reply_to_status_id=tweet.id,auto_populate_reply_metadata=True)
        if any(keyword in tweet.text.lower() for keyword in keywords) == False:
          logging.info(f"Answering to {tweet.user.name}")      
          api.update_status(status=get_quote(),in_reply_to_status_id=tweet.id,auto_populate_reply_metadata=True) 
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "info"], since_id)
        logging.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()

