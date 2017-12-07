# CyberCrime Scrapper

This software scraps Command and Control URLs from [CyberCrime Tracker](http://cybercrime-tracker.net/) and tries to get more information about they, such as:
- It is online?
- It is on Tor Network?
- Where is the server located?
- Which ports are open?
- What web server is running?

### Installing
This is a Python 3 software, and it dependencies are:
- requests, for getting HTML and HTTP information;
- nmap-python, to scan for open ports;
- BeautifulSoup 4, for scrapping the HTML;
- subprocess, to run Unix commands.
