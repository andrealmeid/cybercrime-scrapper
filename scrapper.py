from bs4 import BeautifulSoup
import urllib.request as url
import subprocess

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
        self.server = None
        self.so = None

    def setOnlineStatus(self):
        try:
            url.urlopen("http://" + self.url)
            print(url.urlopen("http://" + self.url).info()['Server'])
            self.online = True
        except Exception as e:
            print(e)
            self.online = False

    def getOnlineStatus(self):
        return self.online

    def setCountry(self):
        u = self.url.find('/')
        p = subprocess.Popen(["geoiplookup", self.url[:u]], stdout=subprocess.PIPE)
        output, err = p.communicate()
        print(output.decode(encoding='UTF-8')[23:])


r = url.urlopen('http://cybercrime-tracker.net/index.php?s=0&m=10').read()

soup = BeautifulSoup(r, 'html.parser')

botnets_list = soup.find('tbody').find_all('tr')

botnets = []

for server in botnets_list:
    data = server.find_all('td')
    bot_info = []
    for d in data:
        bot_info.append(d.text)

    botnets.append(Botnet(bot_info[0], bot_info[1], bot_info[2], bot_info[3]))

#print(url.urlopen("http://dalletenterprisesltd.com.md-hk-7.webhostbox.net/AZORult/").info()['Server'])


for bot in botnets:
    print(bot.family, end=" ")
    bot.setOnlineStatus()
    print(bot.getOnlineStatus())
#     # bot.setCountry()
#
    #u = bot.url.find('/')
    #print(url.urlopen("http://" + bot.url).info()['Server'])
#
