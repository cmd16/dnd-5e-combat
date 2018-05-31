from bs4 import BeautifulSoup
import urllib.request

def read_from_open5e(url):
    soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
    soup = soup.body.div.section.div.div.find_all("div")[1].div.div
    name = soup.h1.get_text().replace("¶", "")
    print("name:", name)
    sections = soup.p
    stuff = ["ac", "hp", "speed", "saving throws", "skills"]
    # print(soup.get_text())

read_from_open5e("https://open5e.com/monsters/monsters_a-z/a/angels/deva.html")
