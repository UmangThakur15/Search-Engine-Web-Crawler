import math
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import json
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient



cachedStopWords = stopwords.words("english")
ps = PorterStemmer()
#Pseudo Relevance ES



#Config Elastic Search
es=Elasticsearch([{"host":"localhost"}],timeout=1000)
index="ap_dataset"
indices = IndicesClient(es)



f = open("./queries_pseudo_es.json")
queries = json.load(f)
#print(queries)


t = open("./parsed_file.json")
parsed_data = list(json.load(t).keys())
#print(parsed_data)


t = open("./index_data.json")
doc_data = json.load(t)
#print(doc_data)


t=open("./index_stat.json")
index_stat=json.load(t)
#print(index_stat,"\n")



def query_token(data):
    body = {
        "tokenizer": "standard",
        "text": data
    }
    token = indices.analyze(index=index, body=body)
    #print("token : ",token)
    return token



def token_c(tok_list, token):
    count = 0
    for t in tok_list:
        if t == token:
            count += 1
    #print(i)
    return count



# To retrieve top scored documents.

def retriveDocs(k):
    f = open('./bm25_result.txt', 'r')
    docNo = []
    i = 0
    for line in f:
        # print("a" + line.split()[3].strip() + "a")
        if (i < k):
            i += 1
            docNo.append(line.split()[2])
    return docNo




def significant_terms(file_name):
    sig_terms = {}
    queries = []
    query_id = []
    with open("./" + file_name, "r") as f:
        for i in f.readlines():
            queries.append(re.findall("[A-Z|a-z].*[a-z]", i))
            query_id.append(re.findall("^[0-9]+", i))
            sentence = [x for xs in queries for x in xs]
            #print("sentence :",sentence)
            q_id = [x for xs in query_id for x in xs]
            #print("q_id :",q_id)
            #final = [[ps.stem(token) for token in sentence.split(" ")
            #          if token not in cachedStopWords] for sentence in sentence if sentence not in cachedStopWords]
            #          if token not in cachedStopWords

            query_sig_list = []
            query_sig_dict = {}
            final= [[ps.stem(token) for token in sentence.split(" ") if token not in cachedStopWords]
                    for sentence in sentence if sentence not in cachedStopWords]
            i=0
            for sublist in final:
                #print("sublist",sublist)
                for key in sublist:
                    #print("key :",key)
                    body = {
                        "query": {
                            "terms": {"text": [key]}
                        },
                        "aggregations": {
                            "significantCrimeTypes": {
                                "significant_terms": {
                                    "field": "text"
                                }
                            }
                        },
                        "size": 0
                    }
                    resp = es.search(index="ap_dataset", body=body)
                    #print("significant ",resp)
                    for bucket in resp['aggregations']['significantCrimeTypes']['buckets']:
                        #print("bucket :", bucket)
                        term = bucket["key"]
                        doc_count = bucket["doc_count"]
                        #print("doc_count :", doc_count)
                        if term in sig_terms:
                            sig_terms[term] += 1
                        else:
                            sig_terms[term] = 1
            i=i+1

    significant_terms = []
    for term, value in sig_terms.items():

        # New term is: relevant to more than 1 other term, not a stop word, not a duplicate
        if value > 0 and term not in cachedStopWords and term not in sig_terms and term not in query:
            significant_terms.append(term)

    # Dictionary of values
    return significant_terms




def es_built_in_query(query_number, new_terms_a,filename):
    for query_number in query_id:
        query=queries



def run_retrieval_models_with_relevance_feedback(query_number, query_term_list):
    original_doc_ids= retriveDocs(doc)


    new_terms_b = significant_terms(query_term_list)
    query_term_list = query_term_list + new_terms_b
    es_built_in_query(query_number, query_term_list, "./queries.json")



#bm25
def compute_bm(tfd, ld, avg_lg, dtf, tfq):
    k1 = 1.2
    k2 = 100
    b = 0.75
    return math.log((84678 + 0.5) / (dtf + 0.5)) * (
                (tfd + (k1 * tfd)) / (tfd + (k1 * ((1 - b) + (b * (ld / avg_lg)))))) * ((tfq + (k2 * tfq)) / (tfq + k2))

score = { "bm25": []}




# Rerun IR model


for query_id, query in queries.items():
    query_tok_details = query_token(query)
    #print(query_id, ": ",query_tok_details)
    query_tokenized = [(tok['token']) for tok in query_tok_details['tokens']]
    #print(query_tokenized,"\n")
    doc_id = set()

    score_bm25_list = []

    for doc in parsed_data:

    #for doc in tqdm(parsed_data):
        #print(doc) #doc id AP..

        tv = doc_data[doc]
        #print(tv) # full data in the index stat file
        #print(tv['term_vectors']) #has all the term vectors details

        if "text" not in tv['term_vectors']:
            continue
        terms = tv['term_vectors']['text']['terms']
        #print(terms) #has doc_freq, ttf, term_freq of all the terms
        score_bm25 = 0

        #print(query_tokenized) #has list of all ther terms in query
        for token in query_tokenized:
            #print(token) #has query term(one word)
            if token not in terms:
                tf = 0
            else:
                tf = terms[token]["term_freq"]
                #print(token,terms[token]) #has the doc_freq, ttf, term_freq of a token
                #print(tf)
            #print("indexed_data ",indexed_data)
            #print("terms[token]",terms[token])
            ttf = index_stat["term"][token]["ttf"]
            #print("ttf: "+token+" "+str(ttf))
            tdf = index_stat["term"][token]["dtf"]
            #print("dtf :"+token+" "+str(tdf))

            tfq = token_c(query_tokenized, token)

            doc_id.add(doc)

            ld = index_stat["doc"][doc]
            #print("ld : ",ld,"\n")

            avg_lg = index_stat["stat"]["avg_doc_length"]
            #print("avg_ld",avg_lg,"\n")

            vocab = index_stat["stat"]["tot_num_words"]
            # print("vocab",vocab,"\n")


            score_bm25 = score_bm25 + compute_bm(tf, ld, avg_lg, tdf, tfq)


        score_bm25_list.append([score_bm25, doc, query_id])



    score_bm25_list.sort(reverse=True)
    score_bm25_list = score_bm25_list[:1000]


    score["bm25"].extend(score_bm25_list)
    # print("bm25 :",score["bm25"],"\n")



for key in score.keys():
    query_doc_es = [str(arr[2]) + " Q0 " + arr[1] + ' ' + str(i + 1) + ' ' + str(arr[0]) + ' Exp\n' for i, arr in
                    enumerate(score[key])]
    file = open(key + "_pseudo_rel_result_es.txt", "w")
    file.writelines(query_doc_es)
    file.close()

#print(query_doc_es)


file_name="queries_pseudo_es.json"
significant_terms(file_name)