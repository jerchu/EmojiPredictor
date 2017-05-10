#@author: Frederica Chen

import json
import sys
import re
from nltk.tokenize import word_tokenize

def remove_emoji(tweets_file, emoji_file):

    wy = open("wy.txt", "w", encoding= "utf-8")
    open_emojiFile = open(emoji_file, 'r', encoding="UTF-8", errors='ignore')
    read_emojiFile = open_emojiFile.read()
    splitNL_emojiFile = read_emojiFile.split('\n')
    
    emoji_arr = []          #emoji_arr is the array of all emojis found in the emoji2vec 
    for i in splitNL_emojiFile:
        emoji_arr.append(i)
        
    
    #regex of URL links
    urls = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    #regex of @mentions in case of retweets
    at_mentions = re.compile(r'(?:@[\w_]+)')
    #regex of html_tags
    html_tags = re.compile(r'<[^>]+>')
    #regex of letters in alphabet
    alpha = re.compile(r'[^a-zA-Z]*')
    #creates a file with extracted tweets with proper format in which the emoji is at the end
    rtweets = open("rtweets_emoji.txt", "w", encoding= "utf-8")

    with open(tweets_file, 'r', encoding="utf-8") as f:
        
        for line in f:
            try: 
                tweet = json.loads(line)
                me = tweet['text']      #retreives tweet from key attribute 'text'
                hey = me.replace('\n',' ')      #replaces newlines within a tweet with spaces
                hey = hey.split(' ')            #splits each tweet based on space
                if alpha.search(hey[0]):    #if the first word in a tweet begins with a word
                    for i in hey:           
                        if '#' in i:
                            rtweets.write(i.replace("#", '')+ " ")
                        elif urls.search(i):
                            rtweets.write(urls.sub("",i))
                        elif at_mentions.search(i):
                            rtweets.write(at_mentions.sub("",i))
                        elif html_tags.search(i):
                            rtweets.write(html_tags.sub("",i))
                        elif i is '\n':
                            rtweets.write(i.replace('\n', ""))
                        elif i[:1] in emoji_arr:
                            rtweets.write(i[:1] + '\n')
                        else:
                            rtweets.write(i)                            
                        rtweets.write(" ")
                
            except Exception as e:
                print("hey" + e)
                

    
remove_emoji("tweets.json", "emojis.txt")


