from bs4 import BeautifulSoup
import nmap
import requests
import subprocess

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
"Accept":"text/html,application/xhtlm+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

class Botnet:
    def __init__(self, date, url, ip, family):
        self.date = date
        self.url = url
        self.ip = ip
        self.family = family
        self.online = False
        self.tor = False
        self.ports = []
        self.country = None
        self.webServer = None
        self.so = None

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
        u = self.url.find('/')
        p = subprocess.Popen(["geoiplookup", self.url[:u]], stdout=subprocess.PIPE)
        output, err = p.communicate()
        self.country = output.decode(encoding='UTF-8')[23:25]


    def checkOpenPorts(self):
        nm = nmap.PortScanner()
        u = self.url.find('/')
        host = self.url[:u]
        nm.scan(host, '1-1000')
        self.ports = list(nm[nm.all_hosts()[0]]['tcp'].keys())

    # Returns True if the C&C server is found online and False otherwise.
    def updateInfo(self):
        self.updateOnlineStatus()
        if self.online:
            self.checkCountry()
            self.updateWebServer()
            self.checkOpenPorts()
            return True
        else:
            return False

    def getCsvData(self):
        return self.url + "; " + str(self.online) + "; " + str(self.country) + "; " + str(self.webServer) + "; " + str(self.ports)

r = requests.get('http://cybercrime-tracker.net/index.php?s=0&m=2').text

soup = BeautifulSoup(r, 'html.parser')

botnets_list = soup.find('tbody').find_all('tr')

botnets = []

for server in botnets_list:
    data = server.find_all('td')
    bot_info = []
    for d in data:
        bot_info.append(d.text)

    botnets.append(Botnet(bot_info[0], bot_info[1], bot_info[2], bot_info[3]))

for bot in botnets:
    if bot.updateInfo():
        print (bot.getCsvData())
