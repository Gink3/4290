from bs4 import BeautifulSoup
import urllib.request
import nltk
from nltk.corpus import stopwords
from nltk.translate.meteor_score import allign_words

# Retrives and processes the spacex wiki page into tokens
response = urllib.request.urlopen('https://en.wikipedia.org/wiki/SpaceX')
html = response.read()
soup = BeautifulSoup(html,"html5lib")
text = soup.get_text(strip=True)
tokens = [t for t in text.split()]
clean_tokens = tokens[:]

# Gets the list of english stop words and removes them from the token list
sr = stopwords.words('english')
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)
    # Try block to test if a token is an integer
    # if so remove token
    # else ignore
    try:
        int(token)
        clean_tokens.remove(token)
    except:
        continue

# Formats the list in a frequency distribution and prints pairs
freq = nltk.FreqDist(clean_tokens)
for key,val in freq.items():
    print (str(key) + ':' + str(val))

# Turns the freqDist item to a list
all_words = list(freq.items())

# Removes items with a count less than 5
all_words_filter = list(filter(lambda x: x[1]>5, all_words))

# creates a list with the same word counts that can be read back into a FreqDist item
all_words = []
for pair in all_words_filter:
    all_words.extend([pair[0]] * pair[1])

freq = nltk.FreqDist(all_words)

# Creates the plot
freq.plot(10,cumulative=False)

import matplotlib.pyplot as plt

# sort the words to get the same results as above
all_words_filter.sort(key=lambda x: x[1], reverse=True)

# x and y for graph
words = [w[0] for w in all_words_filter]
val = [w[1] for w in all_words_filter]

# plot graph
plt.bar(words[:10], val[:10])
plt.show()