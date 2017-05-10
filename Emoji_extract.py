
emojis = []

with open("emoji2vec.txt", 'r', encoding='UTF-8') as f:
    for line in f:
        emojis.append(line.split(" ")[0] + "\n")

with open("emojis.txt", 'w', encoding='UTF-8') as f:
    f.writelines(emojis)
