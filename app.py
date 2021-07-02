from datetime import date
from sqlite3.dbapi2 import Date

from flask import Flask,jsonify,request
from flask_cors import CORS
from utils import add_doc, add_log, db_init, document_check, get_all_docs, get_all_drivers, get_logs, get_static_owner_details, get_static_vehicle_details, license_check, scan_finger 

app =  Flask(__name__)
cors = CORS(app)
@app.route("/")
def ping():
    return "Ping: Successful!"
    
#this is to read from license no and get corresponding fingerprint

@app.route("/verify_license")
def verify_license():
    return license_check()

# this is to  login a  user taking fingerprint

@app.route("/verify_fingerprint" , methods=['POST'])
def verify_fingerprint():
    data = request.get_json()
    print(data)
    if "fingerprint" in data:
        return str(scan_finger(data["fingerprint"]))
    return "0"

# Document 
    # verify docs
@app.route("/verify_documents")
def verify_documents():
    StatusCode = document_check()

    status = {
        0:"Success",
        1:"PUC not found",
        2:"Insurance not found"
    }

    return status.get(StatusCode,"Unexpected error")
    # get all docs
@app.route("/get_all_docs")
def g_a_d():
    return jsonify({"docs":[dict(i) for i in get_all_docs()]})

# get static Information

@app.route("/get_vehicle_details")
def get_vehicle_details():
    return jsonify(get_static_vehicle_details())

@app.route("/get_owner_details")
def get_owner_details():
    return jsonify(get_static_owner_details())


#get Dynamic info

@app.route("/get_all_drivers")
def get_drivers():
    return jsonify({"drivers":[dict(i) for i in get_all_drivers()]})

# Logs
@app.route("/get_all_logs")
def get_all_logs():
    return jsonify({"logs":[dict(i) for i in get_logs()]})

@app.route("/add_log")
def add_new_log(typ,desc):
    return add_log(typ,desc)


#Document add 

@app.route("/add_document" ,methods=['POST'])
def add_new_document():
    dt = request.get_json()
    if "type" in dt and "id" in dt:
        return add_doc(dt["type"],dt["id"], Date(2000,9,12))    
    else:
        return "Bad request"
if __name__ == "__main__":
    db_init()
    app.run()