from pymongo import MongoClient # type: ignore
import hashlib

connection_string="mongodb+srv://hjgoat:hjgoat@technormieshackx.jwvnz.mongodb.net/"
client=MongoClient(connection_string)
db=client["amongus"]
userdata=db["userdata"]
quizdata=db["quizdata"]

def add_signup(useremail,password,name):
    newpass=hashlib.sha256(password.encode()).hexdigest()
    query={"useremail":useremail}
    if userdata.find_one(query):
        return False
    userdata.insert_one({'useremail':useremail,'password':newpass,'name':name,'State':0})
    return True

def check_login(useremail,password):
    newpass=hashlib.sha256(password.encode()).hexdigest()
    query={"useremail":useremail,"password":newpass}
    if userdata.find_one(query):
        return True
    return False

def getName(useremail,password):
    newpass=hashlib.sha256(password.encode()).hexdigest()
    query={"useremail":useremail,"password":newpass}
    projection={"name":1,"_id":0}
    result=userdata.find_one(query,projection)
    return result['name']


def getQuestion(state):
    query={"State":state}
    document=quizdata.find_one(query,{"_id":0})
    return document


def getState(useremail):
    query={"useremail":useremail}
    condition={"_id":0,"State":1}
    result=userdata.find_one(query,condition)
    return result['State']

def IncrementState(email):
    query = {"useremail":email}
    userdata.update_one(query,{'$inc':{"State":1}})
    return True

def DecrementState(email):
    query = {"useremail": email}
    current_data = userdata.find_one(query)
    if current_data and current_data["State"] > 0:
        userdata.update_one(query, {'$inc': {"State": -1}})
        current_data = userdata.find_one(query)
        print(current_data)
        result = quizdata.find_one({"State":current_data["State"]})
        print(result)
        return result
    else:
        result = quizdata.find_one({"State":0})
        return result