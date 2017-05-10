from keras.layers.embeddings import Embedding
from keras.layers import LSTM, GRU
from keras.layers import Dense, Activation, TimeDistributed
from keras.models import Sequential, Model
from keras.layers import Reshape
from keras.layers import Input
from keras.layers import Flatten
from keras.layers.merge import Concatenate
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from gensim.models.keyedvectors import KeyedVectors

import numpy as np

print("Input a Sentence:")
inputstring = input()
inputlen = len(inputstring.split())
predict_texts = [inputstring]

emojis = []

with open("emojis.txt", 'r', encoding='UTF-8') as f:
    for line in f:
        line = line.replace('\n', '')
        emojis.append(line)

train_texts = []
train_emojis = []

with open("rtweets_emoji.txt", 'r', encoding='UTF-8') as f:
    for line in f:
        text = line
        for emoji in emojis:
            if(emoji in line):
                truncated_line = line.replace(emoji, '')
                contains_emoji = False
                for emoj in emojis:
                    if emoj in truncated_line:
                        contains_emoji = True
                if not contains_emoji and len(truncated_line) > 0:
                    train_texts.append(truncated_line)
                    train_emojis.append(emoji)
                    inputlen = max([inputlen, len(truncated_line.split())])

print("converting emojis to vectors...")

emoji2vec_model = KeyedVectors.load_word2vec_format("emoji2vec.bin", binary=True)

#train_emojis = np.reshape(np.asarray(train_emojis), np.asarray(train_emojis).shape + (1,))

#print(train_emojis.shape)

texts = train_texts.copy()
#texts.extend(predict_texts)

print("tokenizing...")

tokenizer = Tokenizer(num_words=inputlen)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
data = pad_sequences(sequences, maxlen=inputlen)
indices = np.arange(data.shape[0])
data = data[indices]
word_index = tokenizer.word_index
embeddings_index = {}

print("retrieving word vectors...")

#with open("GoogleNews-vectors-negative300.txt", 'r', encoding='UTF-8') as f:
    #for line in f:
        #values = line.split()
        #word = values[0]
        #coefs = np.asarray(values[1:], dtype='float32')
        #embeddings_index[word] = coefs
vectors_model = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)
#vectors_model = KeyedVectors.load_word2vec_format("vectors.txt", binary=False)

print("indexing word vectors...")

embedding_matrix = np.zeros((len(word_index) + 1, 300))
for word, i in word_index.items():
    try:
        embedding_vector = vectors_model.word_vec(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector
    except Exception as e:
        print("error with a word")

print("building Model...")
model = Sequential()
model.add(Embedding(len(word_index) + 1, 300, input_shape=data.shape[1:], weights=[embedding_matrix], trainable=False))
model.add(LSTM(300))
model.add(Dense(300))
model.compile(optimizer='adagrad', loss='mse', metrics=['acc'])

print(model.layers[0].output)
print(model.layers[1].output)
print(model.output)

print("extracting emojis vectors...")

emoji_index = {}
embeddings_index = {}
embeddings_emojis = {}

emojiset = set()

with open("emoji2vec.txt", 'r', encoding='UTF-8') as f:
    for line in f:
        values = line.split()
        emoji = values[0]
        emojiset.add(emoji)
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[emoji] = coefs
emojis = []
for emoji in emojiset:
    emojis.append(emoji)
for i in range(len(emojis)):
    emoji_index[emojis[i]] = i
emoji_matrix = np.zeros((len(train_emojis), 300))
embedding_matrix = np.zeros((len(emoji_index) + 1, 300))
for emoji, i in emoji_index.items():
    embedding_vector = embeddings_index.get(emoji)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector
for i in range(len(train_emojis)):
    embedding_vector = embeddings_index.get(train_emojis[i])
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        emoji_matrix[i] = embedding_vector

test_sample = int(0.25 * data.shape[0])

results = model.fit(x=data[:-test_sample], y=emoji_matrix[:-test_sample], epochs=2)
print (results)

loss, acc = model.evaluate(x=data[-test_sample:], y=emoji_matrix[-test_sample:])

print("loss: {}".format(loss))
print("accuracy: {}".format(acc))

print("getting prediction...")

test_texts = train_texts[-test_sample:]
test_emojis = train_emojis[-test_sample:]

predictions = model.predict(data[-test_sample:])
#print(prediction)
'''max_emoji = 0
max_length = 0
for emoji in emoji_index:
    embedding_vector = embeddings_index.get(emoji)
    #print(embedding_vector)
    length = (prediction @ embedding_vector) / np.linalg.norm(embedding_vector)
    if(length > max_length):
        max_emoji = emoji
        max_length = length
#print(max_emoji)'''
with open("emojiout.txt", 'w', encoding='UTF-8') as f:
    for i in range(len(test_texts)):
        f.write("{0} {1}\n {0} {2}\n".format(test_texts[i], test_emojis[i], emoji2vec_model.similar_by_vector(predictions[i])[0][0]))
print(model.output)
