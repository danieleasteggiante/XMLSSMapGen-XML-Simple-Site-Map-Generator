import requests
from bs4 import BeautifulSoup
import re
import threading
         
SITE_MAP = []

def parser(htmlRaw):
    soup= BeautifulSoup(htmlRaw,"html.parser")
    a_list = soup.findAll('a', href=True)
    return a_list


def extractLinks(a_list, domain, base_url):
    for a in a_list:
        href = a.get('href')  
        if len(href) == 1 and href == '/':
            yield base_url
        if domain in href:
            if href[-1] == '/':
                href = href[:-1] 
            yield href
        elif domain not in href and len(href)>1 and 'http' not in href:
            if href[-1] == '/':
                href = href[:-1]    
            if href.startswith('/'):
                yield base_url + href
            elif re.match(r'^[a-z]',href):
                yield base_url + "/" + href
            elif re.match(r'^tel',href):
                yield base_url + "/" + href
            elif re.match(r'#',href):
                continue


def spider(url, domain, baseurl):
    global SITE_MAP
    httpUrl = url.replace("https","http") 
    try:
        req =  requests.get(url)
    except:
        req =  requests.get(httpUrl)     
    content = req.content  
    a_list = parser(content)
    #site_map_tmp = list(set(extractLinks(a_list, domain, baseurl)))
    for elem in extractLinks(a_list, domain, baseurl):
        if elem not in SITE_MAP:
            SITE_MAP.append(elem)

def index_in_list(index, a_list):
    if index < len(a_list):
        return True
    else:
        return False
    
def exploreSite(url):
    global SITE_MAP
    domain = url.split("//")[1]
    SITE_MAP.append(url)
    threads=[]
    counter=0
    spider(SITE_MAP[0],domain,url)
    SITE_MAP = list(set(SITE_MAP))
    flag= True
    while flag:
        print('\rAbbiamo controllato {0} links su {1} trovati'.format(counter, len(SITE_MAP)), end='', flush=True)
        
        for i in range(0,10):
            flag = index_in_list(counter + i, SITE_MAP)
            if flag:
                worker = threading.Thread(target=spider, args=[SITE_MAP[counter+i], domain, url])
                threads.append(worker)
                worker.start()
                counter+=1
            else:
               flag = False 
        
        for el in threads:
            el.join()
    return SITE_MAP

def stampaXml(elenco_url, nome_file="site_map"):
    with open (nome_file + ".xml", "w") as fileXml:
        fileXml.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        print('sto scrivendo il file:')

        for i in elenco_url:
            print(len(elenco_url) - elenco_url.index(i))
            fileXml.write('<url>\n')
            fileXml.write('<loc>' + i + '</loc>\n')
            fileXml.write(' </url>\n')
            
        fileXml.write('</urlset>\n')
        print('Fine processo')

if __name__ == '__main__':
    logo = """
     __   ____  __ _       _____ _ _       __  __          _____   _____            
 \ \ / /  \/  | |     / ____(_) |     |  \/  |   /\   |  __ \ / ____|           
  \ V /| \  / | |    | (___  _| |_ ___| \  / |  /  \  | |__) | |  __  ___ _ __  
   > < | |\/| | |     \___ \| | __/ _ \ |\/| | / /\ \ |  ___/| | |_ |/ _ \ '_ \ 
  / . \| |  | | |____ ____) | | ||  __/ |  | |/ ____ \| |    | |__| |  __/ | | |
 /_/ \_\_|  |_|______|_____/|_|\__\___|_|  |_/_/    \_\_|     \_____|\___|_| |_|
                                                                                                                                                        
    
    """
    print(logo)
    url = ''
    while len(url) < 14:
        if len(url) < 14:
            url= input('Inserire nome valido (es.: https://www.nomesito.it): ')
    file_name = input('inserire nome del file da salvare: ')

    siteMap = exploreSite(url)
    stampaXml(siteMap)
