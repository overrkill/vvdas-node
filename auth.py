from os.path import exists

def get_node_id():

    try:
        if(exists("node/id")):
            with open("node/id") as id:
                return id.read()
        else:
            raise  Exception("-- no node id found -- ")
    except Exception as e:
        print(e)
        return ""
    
def get_key():
    try:
        if(exists("node/pvk")):
            with open("node/pvk") as id:
                return id.read()
        else:
            raise  Exception("-- no key found --")
    except Exception as e:
        print(e)
        return ""


