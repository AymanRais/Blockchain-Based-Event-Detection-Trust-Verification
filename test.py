import pandas as pd
from sklearn.model_selection import train_test_split
from string import punctuation
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

global tfidf_vectorizer

textdata = []
labels = []

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def cleanNews(doc):
    tokens = doc.split()
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [word for word in tokens if len(word) > 1]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = ' '.join(tokens)
    return tokens
'''
dataset = pd.read_csv('Dataset/BuzzFace_fake_news_content.csv')
for i in range(len(dataset)):
    news = dataset.get_value(i, 'text')
    news = str(news)
    news = news.strip().lower()
    labels.append(1)
    clean = cleanNews(news)
    textdata.append(clean)
print("done")
dataset = pd.read_csv('Dataset/BuzzFace_real_news_content.csv')
for i in range(len(dataset)):
    news = dataset.get_value(i, 'text')
    news = str(news)
    news = news.strip().lower()
    labels.append(0)
    clean = cleanNews(news)
    textdata.append(clean)
print("done")
textdata = np.asarray(textdata)
labels = np.asarray(labels)

indices = np.arange(textdata.shape[0])
np.random.shuffle(indices)
textdata = textdata[indices]
labels = labels[indices]
print(textdata.shape)
print(labels.shape)
np.save("model/text",textdata)
np.save("model/labels",labels)

'''


textdata = np.load("model/text.npy")
labels = np.load("model/labels.npy")

tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, use_idf=True, smooth_idf=False, norm=None, decode_error='replace', max_features=3000)
tfidf = tfidf_vectorizer.fit_transform(textdata).toarray()        
df = pd.DataFrame(tfidf, columns=tfidf_vectorizer.get_feature_names())
print(str(df))
print(df.shape)
X = df.values




    
