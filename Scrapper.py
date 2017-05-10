import tweepy
import json
import re

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        with open("tweets.txt", 'a', encoding='UTF-8') as g:
            g.write("{}\n".format(status.text))

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

consumer_key = "YHwzQGTFBc8CNj3arWAzGYD5L"
consumer_secret = "Tobn0yMp5slTnADDM871jntNzEiuKPnK8TissEpQAX90tV7Foy"
access_token = "863652409-0cSZ7temtelTqAZJa63xTk53o9Jzawu1GYaA1qGJ"
access_token_secret = "9fWcnMmkUC51f1vgmbmbxId6HyBZelFJs1fRsKcIxn3aB"

'''
with open("secret.txt", 'r') as f:
    for line in f:
        args = line.split("\t")
        if("consumer_key" in args[0]):
            consumer_key = args[1]
        elif("consumer_secret" in args[0]):
            consumer_secret = args[1]
        elif("access_token" in args[0]):
            access_token = args[1]
        elif("access_token_secret"):
            access_token_secret = args[1]
'''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

emojis = []

with open("emojis.txt", 'r', encoding='UTF-8') as f:
    for line in f:
        emojis.append(line)

print(len(emojis))

print("hooking in...")

#myStream.filter(track=emojis, languages=['en'])
division = (1661 // 180) + 1
with open("tweets.json", 'w', encoding='UTF-8') as f:
    counter = 0
    searchstring = emojis[0]
    for counter in range(180):
        searchstring = '" ' + emojis[counter*division] + '"'
        upperbound = min([(counter + 1) * division, 1661])
        for i in range(counter*division, upperbound):
            searchstring += " OR " + '" ' + emojis[i] + '"'
        results = api.search(searchstring + " -filter:retweets", lang='en', count=100)
        print(counter)
        for tweet in results:
            '''index = tweet.text.find(emoji)
            #text = tweet.text[:index+1]
            text = tweet.text
            if(len(text) > 1):
                text = re.sub('RT \.*:', '', text)
                replace_hashtags = re.findall('#\.* ', text)
                replace_usernames = re.findall('@\.* ', text)
                for hashtag in replace_hashtags:
                    text = text.replace(hashtag, hashtag[1:])
                for username in replace_usernames:
                    text = text.replace(username, username[1:])'''
            f.write("{}\n".format(json.dumps(tweet._json)))

print("*hacker voice* I'm in")
