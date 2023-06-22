import json

f = open("inverted_index_stemmed.json", "r")
inverted_index = json.load(f)

f = open("doc_len_stat_stemmed.json", "r")
doc_len_state = json.load(f)

tok_stat = {}
for word, doc_data in inverted_index.items():
    dtf = len(doc_data.keys())
    ttf = 0
    for v in doc_data.values():
        ttf += len(v)

    tok_stat[word] = {"ttf" : ttf,
                      "dtf" : dtf}

doc_len_state["term"] = tok_stat

save_file = open("index_stat_stemmed.json", "w")
json.dump(doc_len_state, save_file, indent = 6)
save_file.close()