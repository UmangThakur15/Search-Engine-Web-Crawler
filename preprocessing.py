import json
import time
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords



start = time.time()
ps = PorterStemmer()



# reponse=es.indices.create(index='ap_dataset',body=request_body)

cachedStopWords = stopwords.words("english")


# Data tokenizing, lowercase and removing stopwords without stemming
def read_data_unstemmed(data_file):
    doc_id=[]
    doc_data=[]
    f = open('parsed_file.json')
    data = json.load(f)
    c = 0
    for key, value in data.items():
        sentence = sent_tokenize(value)
        #print("sentence",sentence)
        final = [[token.lower() for token in sentence.split(" ")
                  if token not in cachedStopWords] for sentence in sentence if sentence not in cachedStopWords]
        documents = [" ".join(sentence) for sentence in final if sentence not in cachedStopWords]
        value = ' '.join(documents)
        doc_id.append(key)
        doc_data.append(value)
        # print(text)
        #print("doc_id :",doc_id," : ",doc_data)
        c = c + 1
        print(c)
    f.close()
    return doc_id, doc_data




def save_data_unstemmed(key, value):
    data = dict(zip(key, value))
    #print(data)
    with open('doc_data_unstemmed.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)




# Data tokenizing, lowercase and removing stopwords with stemming
def read_data_stemmed(data_file):
    doc_id=[]
    doc_data=[]
    f = open('parsed_file.json')
    data = json.load(f)
    c = 0
    for key, value in data.items():
        sentence = sent_tokenize(value)
        #print("sentence",sentence)
        final = [[ps.stem(token) for token in sentence.split(" ")
                  if token not in cachedStopWords] for sentence in sentence if sentence not in cachedStopWords]
        documents = [" ".join(sentence) for sentence in final if sentence not in cachedStopWords]
        value = ' '.join(documents)
        doc_id.append(key)
        doc_data.append(value)
        # print(text)
        #print("doc_id :",doc_id," : ",doc_data)
        c = c + 1
        print(c)
    f.close()
    return doc_id, doc_data


def save_data_stemmed(doc_id, doc_data):
    data = dict(zip(doc_id, doc_data))
    #print(data)
    with open('doc_data_stemmed.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)





#Reading queries for tokenizing, lowercase and removing stopwords without stemming
def read_queries_unstemmed(file_name):
    queries = []
    queries_id = []
    value = []
    with open("./" + file_name, "r") as f:
        for i in f.readlines():
            queries.append(re.findall("[A-Z|a-z].*[a-z]", i))
            queries_id.append(re.findall("^[0-9]+", i))
            sentence = [x for xs in queries for x in xs]
            q_id = [x for xs in queries_id for x in xs]
            # print(q_id)
            final = [[token.lower() for token in sentence.split(" ")
                      if token not in cachedStopWords] for sentence in sentence if sentence not in cachedStopWords]
            documents = [" ".join(sentence) for sentence in final if sentence not in cachedStopWords]
    # print(len(documents))
    # print(documents,"\n")
    return documents, q_id



def save_query_unstemmed(documents, q_id):
    data = dict(zip(q_id, documents))
    #print(data)
    with open('queries_unstemmed.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)




#Reading queries for tokenizing, lowercase and removing stopwords with stemming
def read_queries_stemmed(file_name):
    queries = []
    queries_id = []
    value = []
    with open("./" + file_name, "r") as f:
        for i in f.readlines():
            queries.append(re.findall("[A-Z|a-z].*[a-z]", i))
            queries_id.append(re.findall("^[0-9]+", i))
            sentence = [x for xs in queries for x in xs]
            q_id = [x for xs in queries_id for x in xs]
            # print(q_id)
            final = [[ps.stem(token) for token in sentence.split(" ")
                      if token not in cachedStopWords] for sentence in sentence if sentence not in cachedStopWords]
            documents = [" ".join(sentence) for sentence in final if sentence not in cachedStopWords]
    # print(len(documents))
    # print(documents,"\n")
    return documents, q_id




def save_query_stemmed(documents, q_id):
    data = dict(zip(q_id, documents))
    #print(data)
    with open('queries_stemmed.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)



def main():
    file_name = "query_desc.51-100.short.txt"
    data_file = "parsed_file.json"
    key,value = read_data_unstemmed(data_file)
    save_data_unstemmed(key,value)
    doc_id,doc_data=read_data_stemmed(data_file)
    save_data_stemmed(doc_id, doc_data)
    documents, q_id = read_queries_unstemmed(file_name)
    save_query_unstemmed(documents, q_id)
    documents, q_id = read_queries_stemmed(file_name)
    save_query_stemmed(documents, q_id)


main()
end = time.time()

print("The time of execution of above program is :", (end - start), "s")
