import json
import re
import sys


# f = open("savedata_without_stopwords.json","r")
# data = json.load(f)

#step 2
f = open("doc_data_stemmed.json","r")
data = json.load(f)


word_id = 1
words_id_dict = {}
tokens = []
token1000 = []
doc_no = 1
doc_len = {}



for doc_id in data.keys():
    text = data[doc_id].lower()
    #print("text", text)
    ind_to_del = []

    if doc_no%1000 == 0:
        tokens.append(token1000)
        token1000 = []

    # print(text)

    # text = text.replace("/[\W_]/g", '')
    # print(text)
    # text = text.split(r'[^a-zA-Z0-9]')

    text = re.findall(pattern=r"\w+(?:\.?\w)*", string=text)
    # print(doc_no)
    # print(text)
    # exit()

    # for i, _ in enumerate(text):
    #     text[i] = re.sub(r'[^a-zA-Z0-9]', '', text[i])

    final_text = []
    for t in text:
        if t != '':
            final_text.append(t)

    doc_len[doc_id] = len(final_text)
    # print()
    # print(final_text)

    for ind, word in enumerate(final_text):
        if word not in words_id_dict:
            words_id_dict[word] = word_id
            word_id += 1

        token1000.append((words_id_dict[word], doc_id, ind))

    doc_no += 1

if len(token1000) != 0:
    tokens.append(token1000)


print(len(tokens))


save_file = open("tokens_stemmed.json", "w")
json.dump({"tokens" : tokens}, save_file, indent = 6)
save_file.close()


save_file = open("words_id_dict_stemmed.json", "w")
json.dump(words_id_dict, save_file, indent = 6)
save_file.close()


save_file = open("doc_len_stat_stemmed.json", "w")
json.dump({"stat" : {"avg_doc_length" : sum(doc_len.values())/len(doc_len.values()),
                     "tot_num_words" : len(words_id_dict)},
           "doc" : doc_len}, save_file, indent = 6)
# print(words_id_dict)
    # break