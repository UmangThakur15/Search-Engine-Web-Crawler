from canonicalization import canonicalization
import queue
from urllib.parse import urlparse, urlunparse, urljoin
from urllib import request
from urllib.error import HTTPError
import requests
import ssl
from os.path import exists
from bs4 import BeautifulSoup as bs
import time
import urllib.robotparser
import json
rp = urllib.robotparser.RobotFileParser()
import jsonpickle




given_seeds = [
    "http://en.wikipedia.org/wiki/Deval_Patrick",
    "http://en.wikipedia.org/wiki/Governor_of_Massachusetts",
    "https://www.nga.org/governor/deval-patrick/",
    "https://www.thehistorymakers.org/biography/honorable-deval-l-patrick"
]



def status_code(url):
    status = 200
    try:
        r = requests.get(url, timeout=(2, 20))
        return r.status_code
    except HTTPError as err:
        return 200
    except:
        return 401
    return status





ignore_words = {'facebook', 'gettyimages', 'video', 'image', 'job', 'password', 'privacy', 'terms', 'about us', '.mp4',
          'coronavirus', 'covid', ".jpg", ".jpeg", ".gif", ".png", ".pdf", ".php", ".ppt", ".doc","htm","xml","homeschoolmasteryacademy",
          "digitalcardfun","partyelf",'accesibility', 'coupons', 'blog', 'russia',"enjoy", 'ukraine', '.mp3', "licenses",".css", "services", "twitter", "search",
          ".json", "signup", '(',".asp", "comment", "slate", "reddit", "shop", "contact", "calculator", "saint"}


status_json_path = "./url_status.json"



if not exists(status_json_path):
    found_domain = set()
    disallowed = set()
    disallowed_domains = set()
    out_link_graph = {}
    in_link_graph = {}
    pq = []
    queue.put(pq)
    q = [canonicalization(lk) for lk in given_seeds]
    for l in q:
        queue.PriorityQueue()
        queue.push(pq, [-100000,l])
    visited = set(q)
    count = 0
else:
    f = open(status_json_path)
    parsed_state = json.load(f)
    found_domain = jsonpickle.decode(parsed_state["found_domain"])
    disallowed = jsonpickle.decode(parsed_state["disallowed"])
    disallowed_domains = jsonpickle.decode(parsed_state["disallowed_domains"])
    out_link_graph = jsonpickle.decode(parsed_state["out_link_graph"])
    in_link_graph = jsonpickle.decode(parsed_state["in_link_graph"])
    pq = parsed_state["pq"]
    visited = jsonpickle.decode(parsed_state["visited"])
    count = parsed_state["count"]



url_ignore = {
  "https://www.usnews.com/news/the-report/articles/2019-02-22/bernie-sanders-elizabeth-warren-and-the-battle-for-new-hampshire",
    "https://www.usnews.com/news/the-report/articles/2019-05-17/elizabeth-warrens-long-game-gambit-in-the-2020-presidential-election"
}

domain_ing = {
    "www.usnews.com"
}



score_url_terms = {"deval" : 3, "patrick": 3, "governor": 2, "businessman" : 1, "politics" : 2, "massachusetts": 0.5, "african" : 2, "government":1,
                    "boston" : 0.5}


imp_domains = {'.gov', '.com', '.net', '.org', '.co', '.edu'}






def wait(rp):
    delay = rp.crawl_delay(useragent="*")
    if delay != None:
        time.sleep(delay+1)
    else:
        time.sleep(1)




def creating_link(link, path):
    ps = urlparse(link)
    return urljoin(f"{ps.scheme}://{ps.netloc}", path)



def fetch(url):

    pars = urlparse(url)
    curr_scheme, curr_domain, curr_path = pars.scheme, pars.netloc, pars.path
    if curr_domain in ["", " ", None]:
        return False,rp
    rp.set_url(urljoin(f"{curr_scheme}://{curr_domain}", 'robots.txt'))

    robo_url = urljoin(f"{curr_scheme}://{curr_domain}", 'robots.txt')
    if curr_domain not in found_domain:
        status = status_code(robo_url)
        found_domain.add(curr_domain)
        print(robo_url)
        if status == 200:
            try:
                site = urllib.request.urlopen(urllib.request.Request(robo_url, headers={'User-Agent': '*'}))
            except TimeoutError as e:
                found_domain.add(curr_domain)
            except:
                disallowed_domains.add(curr_domain)
                return False,rp

            try:
                result = site.read().decode()
            except:
                result = site.read().decode('0x8b')

            for line in result.split("\n"):
                line = line.strip()
                if line.startswith('Disallow'):
                    try:
                        disallowed.add(urljoin(f"{curr_scheme}://{curr_domain}", line.split(': ')[1].split(' ')[0]))
                    except:
                        continue

        elif status == 401 or status == 403:
            disallowed_domains.add(curr_domain)

    if link in disallowed or curr_domain in disallowed_domains:
        return False,rp
    return True,rp



def link_scoring(inlink,link):
    score = 0
    for k in score_url_terms.keys():
        if k in link:
            score -= score_url_terms[k]

    for i in imp_domains:
        if i in inlink:
            score-=1
        if i in link:
            score-=1

    if urlparse(inlink).netloc != urlparse(link).netloc:
        score-=1

    score += len(in_link_graph[link])

    return score





wo_write_text = ""
write_diff = 50
while count < 45000 and not len(pq) == 0:
    # print(pq[:10])
    # print(visited)
    cur_link = queue.pop(pq)[1]
    if cur_link in url_ignore:
        continue

    if urlparse(cur_link).netloc in domain_ing:
        continue


    fetch, rp = fetch(cur_link)
    print(cur_link)
    # print(cur_link)
    # print(fetch)
    flag_ig = False
    for ign in ignore_words:
        # print(link)
        if ign in cur_link:
            # print(ign)
            flag_ig = True
            break
    if flag_ig:
        continue

    if not fetch:
        continue
    wait(rp)
    try:
        req = requests.get(cur_link)
    except:
        continue

    if req.status_code != 200:
        continue
    content_type = req.headers.get('content-type')
    if "htm" not in content_type:
        continue

    soup = bs(req.text, "html.parser")

    try:
        lang = soup.html["lang"]
        print(lang)
        if lang not in ['en', None, ''] and 'en' not in lang:
            continue
    except:
        pass



    para = soup.find_all("p")
    final_text = ""
    for p in para:
        pass
        final_text += p.text

    final_text = ' '.join(final_text.split('\n'))
    final_text = ' '.join(final_text.split())
    count+=1

    title = soup.find('title')
    if title == None or soup.find_all('a') == None:
        continue

    title = title.text

    current_text = ""
    links = []
    temp_links = []
    for link in soup.find_all('a'):
        try:
            link = link.get('href')
            if urlparse(link).netloc == '':
                link = creating_link(cur_link, link)

            link = canonicalization(link)
            link = "http" + link.split("http")[-1]
            temp_links.append(link)
            if link in in_link_graph:
                in_link_graph[link].add(cur_link)
            else:
                in_link_graph[link] = {cur_link}
            if link in visited or link in disallowed or urlparse(link).netloc in disallowed_domains:
                continue
            visited.add(link)
        except:
            continue
        flag = False
        for ign in ignore_words:
            if ign in link:
                flag = True
                break
        if flag:
            continue

        queue.push(links, [link_scoring(cur_link,link),link])
        visited.add(link)

    for i in links:
        queue.push(pq,i)
        visited.add(i[1])
    print("--", len(temp_links))

    if cur_link in out_link_graph:
        pass
        out_link_graph[cur_link].union({i for i in temp_links})
    else:
        out_link_graph[cur_link] = {i for i in temp_links}

    current_text = "<DOC>\n"
    current_text += "<DOCNO>"+cur_link+"</DOCNO>\n"
    current_text += "<HEAD>"+title+"</HEAD>\n"
    current_text += "<TEXT>\n"
    current_text += final_text + "\n"
    current_text += "</TEXT>\n"
    current_text += "</DOC>\n"
    wo_write_text += current_text




    if len(pq) > 50000:
        pq = pq[:50000]




    if count%write_diff==0:
        with open('state.json', 'w') as out_file:
            json_data = {"found_domain" : jsonpickle.encode(found_domain),
                         "disallowed" : jsonpickle.encode(disallowed),
                         "disallowed_domains": jsonpickle.encode(disallowed_domains),
                         "out_link_graph" : jsonpickle.encode(out_link_graph),
                         "in_link_graph": jsonpickle.encode(in_link_graph),
                         "pq":pq,
                         "visited": jsonpickle.encode(visited),
                         "count" : count}
            json.dump(json_data, out_file, sort_keys = True, indent = 4,
                      ensure_ascii = False)


        with open('./Crawled_Data/crawled_data_'+ str(count//write_diff) + '.txt',"w+") as write_file:
            write_file.write(wo_write_text)


        wo_write_text = ""
