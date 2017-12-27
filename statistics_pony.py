#!/bin/python3

import sqlite3 as lite
import matplotlib.pyplot as plt

database_name = 'botnet.db'

con = lite.connect(database_name)

url = []
date = []
ip = []
family = []
online = []
tor = []
ports = []
country = []
webServer = []
os = []
hash = []

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM botnet WHERE family = 'Pony'")

    rows = cur.fetchall()



for row in rows:
    url.append(row[0])
    date.append(row[1])
    ip.append(row[2])
    family.append(row[3])
    online.append(row[4])
    tor.append(row[5])
    ports.append(row[6])
    country.append(row[7])
    webServer.append(row[8])
    os.append(row[9])
    hash.append(row[10])


os_statistic = {}

for elem in os:
    if elem not in os_statistic.keys():
        os_statistic[elem] = 1
    else:
        os_statistic[elem] += 1


webServer_statistic = {}

for elem in webServer:
    if not elem:
        elem = None

    elif "apache" in elem.lower():
        elem = "Apache"

    elif "nginx" in elem.lower():
        elem = "nginx"

    elif "iis" in elem.lower():
        elem = "Microsoft-IIS"

    if elem not in webServer_statistic.keys():
        webServer_statistic[elem] = 1
    else:
        webServer_statistic[elem] += 1

nginx_statistic = {}

for elem in webServer:
    if not elem:
        elem = None

    elif "nginx" in elem.lower():
        if elem not in nginx_statistic.keys():
            nginx_statistic[elem] = 1
        else:
            nginx_statistic[elem] += 1


apache_statistic = {}

for elem in webServer:
    if not elem:
        elem = None

    elif "apache" in elem.lower():
        u = elem.find("(")
        if u != -1:
            elem = elem[:u]
        if elem not in apache_statistic.keys():
            apache_statistic[elem] = 1
        else:
            apache_statistic[elem] += 1

ports_statistic = {}

for elem in ports:
    p = elem[1:-1].split(", ")

    for port in p:
        if port not in ports_statistic.keys():
            ports_statistic[port] = 1
        else:
            ports_statistic[port] += 1


family_statistic = {}

for elem in family:
    if elem not in family_statistic.keys():
        family_statistic[elem] = 1
    else:
        family_statistic[elem] += 1

country_statistic = {}

for elem in country:
    if elem not in country_statistic.keys():
        country_statistic[elem] = 1
    else:
        country_statistic[elem] += 1

hash_statistic = {}

for elem in hash:
    if elem not in hash_statistic.keys():
        hash_statistic[elem] = 1
    else:
        hash_statistic[elem] += 1

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = val=int((pct*total/100.0)+0.5)
        return '{p:.2f}%  [{v:d}]'.format(p=pct,v=val)
    return my_autopct

def piePlot(dictonary, tolerance=0, explode=None):
    labels = list(dictonary.keys())

    dictonary['Others'] = 0
    for i in range(0, len(labels)):
        if dictonary[labels[i]] < tolerance:
            dictonary.pop(labels[i], None)
            dictonary['Others'] += 1

        #elif dictonary[labels[i]] > 140:
        #    dictonary.pop(labels[i], None)

    if dictonary['Others'] == 0:
        dictonary.pop('Others', None)

    labels = list(dictonary.keys())
    sizes = list(dictonary.values())

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, explode=explode, autopct=make_autopct(sizes), startangle=90)
    ax1.axis('equal')

    plt.show()

top_ports = []

top_ports.append(sorted(ports_statistic.values(), reverse=True))
top_ports.append(sorted(ports_statistic, key = ports_statistic.get, reverse=True))

for i in range(0, 15):
    print(top_ports[1][i], ": ", top_ports[0][i])

#piePlot(family_statistic, 15)
#piePlot(ports_statistic, 200)
#piePlot(os_statistic, explode=(0.1, 0, 0, 0.2))
#piePlot(webServer_statistic, 5, (0, 0, 0, 0.1))
#piePlot(apache_statistic, 3, (0, 0, 0, 0.1))
#piePlot(nginx_statistic, 3)
#piePlot(country_statistic, 5)

piePlot(hash_statistic, 4)

#print(ports_statistic)
#print(apache_statistic)
#print(os_statistic)
#print(webServer_statistic)
