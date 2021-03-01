from bs4 import BeautifulSoup
import requests

def crawl(url, visits, base, ss):
    print(url)
    count = 1
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    ss.append(soup)
    for link in soup.find_all('a'):
        ext = link.get('href')
        if ext is not None and not ext in visits:
            visits[ext] = True
            if ext[0] == '/':
                count += crawl(url+ext, visits, base, ss)
            elif base in ext:
                count += crawl(ext, visits, base, ss)
    return count
supersoup = []
url = input("Enter a URL to crawl: ")
print(crawl(url, {url: True}, url[12:len(url)], supersoup))
print(supersoup)
