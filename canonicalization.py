from urllib.parse import urlparse, urlunparse, urljoin
import re


def canonicalization(url):
    url = url.lower()

    url = urlparse(url)
    path = url.path
    path = path.split("/")
    for i in range(len(path)-1,-1,-1):
        if path[i] == "":
            del path[i]
    path = "/".join(path)


    path = path.split(":")
    if path[-1].isnumeric():
        path = path[:-1]
    path = ":".join(path)

    base = urlunparse((url.scheme, url.netloc, "", "", "", ""))

    final_url = urljoin(base, path)
    if re.match("^(?:\.{2}/)+\w+.*", final_url):
        replace = re.findall("\.{2}/\w+.*", path)[0][2:]
        level = len(re.findall("\.{2}", path))
        folders = re.findall("/\w+(?:\.\w+)*", base)
        target = "".join(folders[-level-1:])
        final_url = re.sub(target, replace, base)

    return final_url


#print(canonicalization("https://abc.com#345"))
