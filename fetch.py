import os, sys
import requests
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime


def soupfindAllnSave(pagefolder, url, soup, metadata, tag2find='img', inner='src'):
    if not os.path.exists(pagefolder):
        os.mkdir(pagefolder)
    count = 0
    for res in soup.findAll(tag2find): 
        try:
            count += 1
            filename = os.path.basename(res[inner])  
            fileurl = urljoin(url, res.get(inner))
            filepath = os.path.join(pagefolder, filename)
            res[inner] = os.path.join(os.path.basename(pagefolder), filename)
            if not os.path.isfile(filepath):
                with open(filepath, 'wb') as file:
                    filebin = session.get(fileurl)
                    file.write(filebin.content)
        except Exception as exc:      
            continue

    if metadata:
        if tag2find == 'img':
            print("images: " + str(count))
        
        elif tag2find == 'link':
            print("num_links: " + str(count))
    return soup

def savePage(response, metadata, pagefilename='page'):    
   url = response.url
   soup = BeautifulSoup(response.text, "html.parser")
   pagefolder = pagefilename+'_files' 
   if metadata:
    print("site: " + pagefilename)
   soup = soupfindAllnSave(pagefolder, url, soup, metadata, 'img', inner='src')
   soup = soupfindAllnSave(pagefolder, url, soup, metadata, 'link', inner='href')
   soup = soupfindAllnSave(pagefolder, url, soup, metadata, 'script', inner='src')
   if metadata:
    now = datetime.now()
    print("last_fetch " + now.strftime("%B %d, %Y %H:%M:%S"))   
   with open(pagefilename+'.html', 'w') as file:
      file.write(soup.prettify())
   return soup


session = requests.Session()
parser = argparse.ArgumentParser()
parser.add_argument('--pages', nargs='+', default=[])
parser.add_argument('--metadata', action='store_true')
args = parser.parse_args()
pages = args.pages

for page in pages:
    try:
        sub = page.find("www.")
        sub = sub + 4 if sub > 0 else page.find("//") + 2
        output = page[sub : ]
        response = session.get(page)
        savePage(response, args.metadata, output)
    except Exception as exc:      
        print(exc, file=sys.stderr)