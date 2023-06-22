import ssl
import urllib.robotparser
from tqdm import tqdm
import json
import jsonpickle


ssl._create_default_https_context = ssl._create_unverified_context

rp = urllib.robotparser.RobotFileParser()

status_json_path = "url_status.json"



f = open(status_json_path)
parsed_state = json.load(f)
out_link_graph = jsonpickle.decode(parsed_state["out_link_graph"])
in_link_graph = jsonpickle.decode(parsed_state["in_link_graph"])



f = open("prepocessed_data.json")
text_data = json.load(f)



final_data = {}
for link in tqdm(text_data.keys()):
    if link not in in_link_graph or link not in out_link_graph:
        continue
    d = {"inlinks" : list(in_link_graph[link]),
         "outlinks" : list(out_link_graph[link]),
         "text" : text_data[link],
         "author" : "Umang"}

    final_data[link] = d



save_file = open("merged_data.json", "w")
json.dump(final_data, save_file, indent = 6)
save_file.close()


