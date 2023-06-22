import json
import re

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

porter = PorterStemmer()


with open("./stoplist.txt") as stop_f:
    stopwords = [word.strip() for word in stop_f]
pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')



def stemming(sentence):
    token_words=word_tokenize(sentence)
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

f = open("parsed_data.json", "r")
parsed_json = json.load(f)


doc_token_json = {}
for link, doc_text in parsed_json.items():
    doc_text = doc_text.replace('\n', " ")
    doc_text = pattern.sub('',doc_text)
    doc_text = stemming(doc_text)
    doc_token_json[link] = doc_text


save_file = open("prepocessed_data.json", "w")
json.dump(doc_token_json, save_file, indent = 6)
save_file.close()

