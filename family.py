#!/bin/python3
from bs4 import BeautifulSoup
import requests

cybercrime_html = requests.get('http://cybercrime-tracker.net/index.php?s=' + '0' + '&m=' + '11000').text
cybercrime_html = BeautifulSoup(cybercrime_html, 'html.parser')
botnetsQueue = cybercrime_html.find('tbody').find_all('tr')

global families

families = {}

def insertFamily(family, date, url):
    global families

    if family not in families.keys():
        families[family] = Botnet(family)

    families[family].dates.append(date)
    families[family].urls.append(url)
    if ".onion" in url:
        families[family].tor += 1

    families[family].count += 1

class Botnet:
    def __init__(self, family):
        self.dates = []
        self.urls = []
        self.tor = 0
        self.count = 0
        self.family = family

while len(botnetsQueue):
    server = botnetsQueue.pop(0)
    data = server.find_all('td')
    bot_info = []
    for d in data:
        bot_info.append(d.text)

    insertFamily(bot_info[3], bot_info[0], bot_info[1])
    #print(bot_info[0], bot_info[3])

for f in families:
    if families[f].tor >= 1:
        print(f)
        print(families[f].count)
        print(families[f].tor)
    #print(families[f].dates)
    #print(families[f].urls)
