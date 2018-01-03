#!/bin/python3

import sqlite3
import os

database_name = 'botnet.db'

if os.path.exists(database_name):
    os.remove(database_name)
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE Botnet (
        url text,
        include_date date,
        ip text,
        family text,
        online boolean,
        tor boolean,
        ports text,
        country text,
        webServer text,
        os text,
        osVersion text,
        hash text,
        dnsRedirect boolean,
        UNIQUE(url)
    )
""")


conn.commit()
conn.close()
