Emoji_extract.py
This file generates an output file "emojis.txt" of the emojis. It reads the first "word" in each line in emoji2vec.txt in encoding "UTF-8" 
and then appends the emoji found to an array. Then it writes each emoji to a newline in "emojis.txt."

Scrapper.py

This file queries the twitter REST API for any tweets containing emojis up to 180 times per run of the program.
The authentication data is extracted from a text file called "secret.txt" following this format:

Consumer_Key:(\t)XXXXXXXXXXXXXXXXXX
Consumer_Secret:(\t)XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Access_Token:(\t)XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Access_Token_Secret:(\t)XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The tweets are output in a json format to "tweets.json"

parseTweets.py

This file contains a function called parse_emoji(tweets_file, emoji_file). 
tweets_file refers to the JSON formatted tweets file (in this case, we used "tweets.json" generated from Scrapper.py) 
and emoji_file refers to the file that contains all the emojis from emoji2vec (in this case, we used "emojis.txt" generated from Emoji_extract.py). 
This function first generates an emoji array. We do so by reading the emoji_file in encoding "UTF-8" and then look at each line (containing the emoji)
and puts it into emoji_arr. Then the function opens the JSON file of the tweets and parses through it. Each line of the JSON file contains a different
tweet and to get the tweet itself we had to retrieve the tweet from key attribute 'text'. Within each tweet, the user might have used newline characters
so we replaced them with a space. Then we looked at each word in the tweet. If it is a hashtag like #awesome, then we removed the # and kept "awesome."
Then we removed URL links, @ mentions, and html tags. Next we wanted to make sure that there is an emoji at the end of each sentence and not a sequence 
of them. When we reached an emoji, we separated the tweet into two different phrases. For example, “OMG I LOVE DOGS 🐶 I could just pet them all day! 😍” 
would be split into “OMG I LOVE DOGS 🐶” and “I could just pet them all day! 😍.” (Set encoding in Notepad++ to UTF-8 to read the emoji if it looks funny).
We then wrote each of these parsed tweets to an output file rtweets_emoji.txt so that our LSTM.py can use the parseTweets.

LSTM.py

This python file contains the model for the LSTM as well as the parser that seperates the data into a sentence and a target.
To run the file, run the file in python 3.5 with the keras, gensim, and tensorflow libraries all installed as well as their dependencies
the program will first extract the emoji and word vectors from the bins "emoji2vec.bin" and "GoogleNews-vectors-negative300.bin", then it will run build the model and run training followed by an evaluation, outputing accuracy as it goes.
Lastly the program will output a file containing each sentence with it's proper emoji followed by the sentence with the guessed emoji into a file called "emojiout.txt".
