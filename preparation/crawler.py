import requests
from bs4 import BeautifulSoup
from dateutil import parser
from pytz import timezone
import pandas as pd

def crawl_page(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.find_all("h1")[1].text

    content = soup.select("p")
    content = "\n".join(c.text for c in content)

    time = soup.select("time")[0].attrs['datetime']
    time = parser.parse(time).astimezone(timezone('Asia/Taipei'))
    time = str(time)

    provider = soup.find_all("div", {"data-reactid": 9})[0]
    provider = provider.find_all("a")[1].text

    data = [title, content, time, provider, url]
    return data

if __name__ == "__main__":
    urls = pd.read_csv("crawler_urls.csv", header=None)
    urls = urls[0].tolist()

    news = []
    n = 0
    for url in urls:
        n += 1
        try:
            data = crawl_page(url)
            news.append(data)
            print "success:", n
        except:
            print "error:", url
    df = pd.DataFrame(news)
    df.columns = ['title', 'content', 'time', 'provider', 'url']
    df.to_csv("news.csv", index=False, encoding='utf-8')