# Imports
from decrypt import decrypt
from rfid import getrfid
from finger import get_finger
import sqlite3
import json
import requests
# DB Connection and initializations

def get_connection():
    return sqlite3.connect("node.db")

def db_init():
    conn = get_connection()
    conn.execute( 'create table if not exists drivers (id INTEGER primary key autoincrement,name TEXT , dl TEXT unique)')
    conn.execute( 'create table if not exists logs (id INTEGER primary key autoincrement,type TEXT , desc TEXT,time DATETIME default current_timestamp)')
    conn.execute( 'create table if not exists documents (id integer , docname TEXT primary key, valid_till DATE)')
    conn.close()

# RIDE check

    #check for a valid license 
def license_check():
     print("Waiting  for license")
     dl = getrfid().strip()
     print("license scanned is ... "+dl)
     vid = open("node/vid").read()
     url = "https://virt-api.herokuapp.com/api/license/retrieve"
     body = {"vid":vid,"dl":dl }
     x = requests.post(url,body)
     obj = decrypt(x.text)
     return obj

    # check for a valid fingerprint
def scan_finger(fingerprint):
    return get_finger(fingerprint)

    #go through document check
def document_check():
    # no Error status code 0 
    ins = False
    puc = False
    rows  = get_all_docs()
    print(rows)
    for i in rows:
        print(i)
        if i["docname"] == "PUC":
            puc = True
        if i["docname"] == "INS":
            ins = True

    if not puc : 
        return 1
    elif not ins:
        return 2
    else:
        return 0


# Driver related stuffs 

def get_all_drivers():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    conn.commit()
    cur.execute('select * from drivers')
    rows = cur.fetchall()
    return rows

def add_driver(name:str,dl:str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("replace into drivers(name,dl) values(?,?)",(name,dl))
    conn.commit()
    conn.close()
    return "driver added"


# Logging related stuff
    # get all logs
def get_logs():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # cur.execute('insert into drivers (name,dl) values(?,?)',("abhi","1231231234"))
    cur.execute('select * from logs order by time desc')
    rows = cur.fetchall()
    return rows

    # add a new log with typw and desc
def add_log(typ:str,desc:str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("insert into logs(type,desc) values(?,?)",(typ,desc))
    conn.commit()
    conn.close()
    return "log added"


# get static info about vehicle and owner details

def get_static_vehicle_details():
    with open("node/vehicle_details.json") as vdf:
        data =  json.load(vdf)
        return data

def get_static_owner_details():
    with open("node/owner_details.json") as odf:
        data =  json.load(odf)
        return data



# Documents
    # Add Document
def add_doc(typ,id,valid):
    conn = get_connection()
    cur = conn.cursor()
    print(cur.execute("replace into documents values(?,?,?)",(id,typ,valid)).lastrowid)
    conn.commit()
    conn.close()
    return "document added"

    # Get All Documents
def get_all_docs():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # cur.execute('insert into drivers (name,dl) values(?,?)',("abhi","1231231234"))
    cur.execute('select * from documents ')
    rows = cur.fetchall()
    return rows
