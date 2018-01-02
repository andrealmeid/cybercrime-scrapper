#!/bin/python3
from bs4 import BeautifulSoup
import nmap
import requests
import subprocess
import sys
import hashlib as hash
import sqlite3 as sql
import threading
from time import sleep


headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
"Accept":"text/html,application/xhtlm+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

#For interthread communication. Maybe there's a better way?
botnetsCount = 0
botnetsReady = []
botnetsQueue = []

#Max threads possible.
maxThreadCount = 1

class Botnet:
    def __init__(self, date, url, ip, family):
        self.date = date
        self.url = url
        self.ip = ip
        self.family = family
        self.online = False
        self.tor = False
        self.ports = None
        self.country = None
        self.webServer = None
        self.os = None
        self.osVersion = None
        self.hash = None

    # Obtain server status
    def updateOnlineStatus(self):
        try:
            r = requests.get("http://" + self.url, headers = headers)
            if r.status_code == 200:
                self.online = True
            else:
                self.online = False

        except requests.exceptions.ConnectionError:
            self.online = False

    def checkTorNewtork(self):
        if ".onion" in self.url:
            self.tor = True

    # Obtains web server
    def updateWebServer(self):
        try:
            r = requests.get("http://" + self.url, headers = headers)
            if r.headers['server'] != None:
                self.webServer = r.headers['server']

        except:
            return

    # Obtains country
    def checkCountry(self):
        p = subprocess.Popen(["geoiplookup", getDomain(self.url)], stdout=subprocess.PIPE)
        output, err = p.communicate()
        self.country = output.decode(encoding='UTF-8')[23:25]

    def checkOpenPorts(self):
        nm = nmap.PortScanner()
        u = self.url.find('/')
        host = self.url[:u]
        nm.scan(host, arguments='-Pn')
        self.ports = str(list(nm[nm.all_hosts()[0]]['tcp'].keys()))

    def checkOsVersion(self):
        nm = nmap.PortScanner()
        nm.scan(self.ip, arguments='-O')
        self.ip = nm[self.ip]['osmatch'][0]['name'])

    def checkOS(self):
        if not self.webServer:
            return

        webServer = self.webServer.lower()

        if webServer.find("ubuntu") != -1:
            self.os = "Ubuntu"
            return

        if webServer.find("centos") != -1:
            self.os = "CentOS"
            return

        if webServer.find("debian") != -1:
            self.os = "Debian"
            return

        if webServer.find("unix") != -1:
            self.os = "Unix"
            return

        if webServer.find("win") != -1 or webServer.find("windows")  != -1 or webServer.find("microsoft")  != -1 or webServer.find("iis") != -1:
            self.os = "Windows"
            return

    def getHtmlHash(self):
        r = requests.get("http://" + self.url, headers = headers).text
        h = hash.md5(str.encode(r))
        self.hash = h.hexdigest()

    # Returns True if the C&C server is found online and False otherwise.
    def updateInfo(self):
        self.checkTorNewtork()
        if self.tor:
            if not ".link" in self.url:
                u = self.url.find('/')
                if u == -1:
                    self.url = self.url + ".link"
                else:
                    self.url = getDomain(self.url) + ".link" + self.url[u:]

        self.updateOnlineStatus()
        if self.online:
            self.checkCountry()
            self.updateWebServer()
            self.checkOpenPorts()
            self.checkOS()
            self.checkOsVersion()
            self.getHtmlHash()
            return True
        else:
            return False

    def getCsvData(self):
        return self.date + "; " + self.url + "; " + self.ip + "; " + self.family + "; " + str(self.online) + "; " + str(self.tor) + "; " + str(self.country) + "; " + str(self.ports) + "; "  + str(self.webServer) + "; "  + str(self.os) + "; " + str(self.hash)

def handleArguments(argv):
    if len(argv) == 1:
        list_start = "0"
        list_size = "30"

    elif len(argv) == 2 and (argv[1] == "--help" or argv[1] == "-h"):
        print("A scrapper to get information about botnets found on http://cybercrime-tracker.net/\n")
        print("List start determines the first botnet to start the list")
        print("List size determines how many botnets you want to scan")
        print("\nUsage: ./scrapper [list start] [list size] [-h|--help]")
        exit(0)

    elif len(argv) == 3:
        try:
            list_start = int(argv[1])
            list_size = int(argv[2])
            if list_start >= 0 and list_size > 0:
                list_start = str(list_start)
                list_size = str(list_size)
            else:
                raise Exception

        except:
            print("Usage: ./scrapper [list start] [list size] [-h|--help]")
            exit(0)

    else:
        print("Usage: ./scrapper [list start] [list size] [-h|--help]")
        exit(0)

    return list_start, list_size

def connectDatabase(database_file):
    try:
        connection = sql.connect(database_file)
        return connection

    except Error as e:
        print("Error connecting to database.")
        print(e)
        sys.exit(1)

def insertDatabase(connection, arg_list):
    global botnetsCount
    try:
        connection.cursor().execute("INSERT INTO Botnet (url, include_date, ip, family, online, tor, ports, country, webServer, os, hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" , arg_list)
        connection.commit()

        print ("Fetched botnet #" + str(botnetsCount) + " - " + arg_list[0])
        botnetsCount += 1

    except Exception as e:
        print("Database insertion error:")
        print(e)


def getDomain(url):
    u = url.find('/')
    return url[:u]

#Threading stuff
def scanUrlList():
    global botnetsCount
    global botnetsReady
    global botnetsQueue

    while len(botnetsQueue):
        server = botnetsQueue.pop(0)
        data = server.find_all('td')
        bot_info = []
        for d in data:
            bot_info.append(d.text)

        if bot_info[2] == "":
            bot_info[2] = getDomain(bot_info[1])

        bot = Botnet(bot_info[0], bot_info[1], bot_info[2], bot_info[3])
        try:
            if bot.updateInfo():
                # print ("Fetched botnet #" + str(botnetsCount) + " - " + bot.url)
                botnetsReady.append(bot)
            else:
                botnetsCount += 1
                print ("Failed to fetch botnet #" + str(botnetsCount) + " - " + bot.url)
        except Exception as e:
            botnetsCount += 1
            print ("Failed to fetch botnet #" + str(botnetsCount) + " - " + bot.url + " - " + str(e))
        sleep(1)



def fireThreadScanUrlList():
    threading.Thread(target=scanUrlList).start()

def main(argv):
    global botnetsReady
    global botnetsCount
    global botnetsQueue
    global maxThreadCount

    list_start, list_size = handleArguments(argv)

    connection = connectDatabase('botnet.db')

    cybercrime_html = requests.get('http://cybercrime-tracker.net/index.php?s=' + list_start + '&m=' + list_size).text
    cybercrime_html = BeautifulSoup(cybercrime_html, 'html.parser')
    botnetsQueue = cybercrime_html.find('tbody').find_all('tr')

    #Firing threads
    for i in range(min(maxThreadCount, int(list_size))):
        fireThreadScanUrlList()

    #Syncronously adding to database:
    while (botnetsCount < int(list_size)) or (len(botnetsReady) > 0):
        if (len(botnetsReady) > 0):
            bot = botnetsReady.pop(0)
            insertDatabase(connection, (
                bot.url, bot.date, bot.ip, bot.family, bot.online, bot.tor, bot.ports, bot.country, bot.webServer, bot.os,
                bot.hash))
        sleep(0.5)

if __name__ == "__main__":
    main(sys.argv)
