import bs4 as bs
import lxml
import urllib.request
import re
import nltk as nltk
import heapq

#Scrapen der Daten vom angegeben URL
scraped_data = urllib.request.urlopen("https://en.wikipedia.org/wiki/Artificial_intelligence")
#Lesen der gescrapten Daten
article = scraped_data.read()

#Parsen der Daten mithilfe eines BeautifulSoup Objectes
parsed_article = bs.BeautifulSoup(article, 'lxml')
#Parsen alles Textes innerhalb der <p> Tags auf Wikipedia
paragraphs = parsed_article.find_all('p')

article_text = ''
for p in paragraphs:
    article_text+= p.text

#Reguläre Ausdrücke um die Referenzen innerhalb des Artikels auszuschließen
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

#Reguläre Ausdrücke um special characters und Zahlen auszuschließen
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


#Tokenizing in Sätze
sentence_list = nltk.sent_tokenize(article_text)
stopwords = nltk.corpus.stopwords.words('english')

#Gewichtete Häufigkeit
#Auflisten aller Wörter mit ihrer Häufigkeit
word_frequencies = {}
tokenized_words = nltk.word_tokenize(formatted_article_text)
for word in tokenized_words:
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequency = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

#Erstellung eines Dictionaries mit allen Sentences -> Score errechnet sich daraus wie häufig die Wörter in diesem Text sind
sentence_scores = {}
for sent in sentence_list:
    words_in_sentence = nltk.word_tokenize(sent.casefold())
    for word in words_in_sentence:
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 25:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
summary = ""
for sent in summary_sentences:
    summary += sent + "\n"
print(summary)
