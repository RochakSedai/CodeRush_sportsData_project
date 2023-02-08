from numpy import vectorize
import sklearn
import nltk
import pickle
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
import string
from nltk.corpus import stopwords

def input_process(text):
    translator = str.maketrans('', '', string.punctuation)
    nopunc = text.translate(translator)
    words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]    #list comprehension method : maxm list operation lai single line of code ma lekhne
    return ' '.join(words)

def load_model_and_vectorizer():
    model = pickle.load(open('classifier.model', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    return model, vectorizer

if __name__ == '__main__':
    model, vectorizer = load_model_and_vectorizer()
    path = input('Enter path of file: ')
    doc = PyPDF2.PdfReader(path)
    page_count = len(doc.pages)
    content = ''
    for page_number in range(page_count):
        page = doc.pages[page_number]
        content = content + page.extract_text()

    content = input_process(content)
    content = vectorizer.transform([content])
    pred  = model.predict(content)
    if pred[0] == 1:
        print('This document is about Cricket..')
    else:
        print('This document is about Football..')

        