import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
from requests_html import HTMLSession

#Output text in different colors in console. Colors are defined here

colorama.init()
GREEN=colorama.Fore.GREEN
GRAY=colorama.Fore.LIGHTBLACK_EX
RESET=colorama.Fore.RESET
YELLOW=colorama.Fore.YELLOW

#Crawler is only concerned with finding internal links. Setting global variable
internal_urls=set()
total_urls_visited = 0


#function to differentiate URLS from JS clickable events/functions
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#Function to returns all internal links
#netloc is the domain name of the website
def get_all_website_links(url):
    #Using set() to ensure no duplication
    urls = set()
    domain_name = urlparse(url).netloc
    session=HTMLSession()
    response =session.get(url)

    #Get Javascript elements as well
    try:
        response.html.render()
    except:
        pass

    #Soup object gets all HTML elements from given URL
    soup=BeautifulSoup(response.html.html,"html.parser")
    #soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href=a_tag.attrs.get("href")
        if href=="" or href is None:
            continue
        #Joining partial href with netloc to get complete URL
        href=urljoin(url,href)
        parsed_href=urlparse(href)
        #Removing GET parameters to get only URL
        href=parsed_href.scheme+"://"+parsed_href.netloc+parsed_href.path

        if not is_valid(href):
            continue

        if href in internal_urls:
            continue

        if domain_name not in href:
            #Not concerned with external URLS so skipping those
            continue

        print (f"{GREEN}[*]Internal Link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

def crawl(url, max_urls=50):
    
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links=get_all_website_links(url)
    for link in links:
        if total_urls_visited>max_urls:
            print("MAX URLS REACHED")
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    crawl(url, max_urls=max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    
    print("[+] Total URLs:",  + len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)

    domain_name = urlparse(url).netloc

    #with open(f"{domain_name}_internal_links.txt", "w") as f:
        #for internal_link in internal_urls:
            #print(internal_link.strip(), file=f)

    with open("internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)