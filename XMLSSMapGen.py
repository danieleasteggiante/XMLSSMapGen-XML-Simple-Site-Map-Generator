import requests
from bs4 import BeautifulSoup
import re

def cercaUrl(url, filtro, stringUrl):
    links= []
    httpUrl = url.replace("https","http")
    try:
        req =  requests.get(url)
    except:
        req =  requests.get(httpUrl)
    content = req.content

    soup= BeautifulSoup(content,"html.parser")

 
    for link in soup.findAll('a', href=True):
        try:
            if filtro in link.get('href'):
                links.append(link.get('href'))
            elif filtro not in link.get('href'):
                if "http" not in link.get('href'):
                    if link.get('href').startswith('/'):
                        links.append(stringUrl + link.get('href'))
                    elif re.match(r'^[a-z]',link.get('href')):
                        links.append(stringUrl + "/" + link.get('href'))
                    elif re.match(r'^tel',link.get('href')):
                        links.append(stringUrl + "/" + link.get('href'))
                    elif re.match(r'#',link.get('href')):
                        continue
                    
        except:
            print('error')
            print(link)
            continue


    return links

def cercaUrl2(lista, filtro, stringUrl):
    lista_url=[]
    lista_url.extend(lista)
    gia_controllati=[]
    url_finali = []
    ind = -1
    while len(gia_controllati) < len(lista_url):
        gia_controllati.append(lista_url[ind])
        ind = ind + 1
        print('gia controllati: ')
        print(len(gia_controllati))
         
        if lista_url[ind] in gia_controllati:
            print('ce----------------' + lista_url[ind] )
        else:
            try:
                new_link = cercaUrl(lista_url[ind],filtro, stringUrl)
                url_finali.append(lista_url[ind])
                print(len(lista_url))
                print(lista_url[ind])
                for i in new_link:
                    if i in lista_url:
                        print('gia inserito')
                    else:
                        lista_url.append(i)
            except TypeError:
                pass

    return url_finali

def stampaXml(elenco_url, nome_file):
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

url = input('inserire url:')
filtro = url.split("//")[1]
stringUrl = url
elenco_home = cercaUrl(url,filtro, stringUrl)
elenco_sito = cercaUrl2(elenco_home,filtro, stringUrl)
print('--------------')
stampaXml(elenco_sito,filtro)
