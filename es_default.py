from elasticsearch import Elasticsearch
import json


#Config Elastic Search
es=Elasticsearch([{"host":"localhost"}],timeout=1000)


query_id = []
query = []
score= []
id =[]
index=[]


def access_query(filename,query,query_id):
    f=open(filename)
    data = json.load(f)
    e = 0
    d=0
    list = []

    for key, value in data.items():
        c = 0
        file = open('output_gen.txt', 'w')
        query_id.append(key)
        query.append(value)
        client = Elasticsearch()
        index = "ap_dataset"
        doc = {
            "size": 1000,
            "query": {
                "match": {"text": value
                              }
                }
            }
        resp = es.search(index=index,
                             body=doc)
        for hit in resp['hits']['hits']:
            c = c + 1
            #print(c)
            #print(key,"Q0" ,hit["_id"],c,hit["_score"],"Exp")
            list.append(str(key)+" Q0 "+str(hit["_id"])+" "+str(c)+" "+str(hit["_score"])+" Exp")
        #e=e+1
    #return query,query_id
    file = open('output_gen.txt', 'w')
    for item in list:
        file.write(item + "\n")
    file.close()


def main():
    access_query("queries.json",query,query_id)
    #output_file(query_id, id,score,rank)

main()