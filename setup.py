import os, hashlib, re, sys
from pathlib import Path

storagePath = os.getcwd() + "/static/STORAGE/"
userDatabasePath = os.getcwd() + "/static/Database/userdatabase.db"
pattern = re.compile("{\"username\":\"(.*)\";\"password\":\"(.*)\"}")

def Run():        
    command = input("Enter a command for: \nAdd User [-n]\nDelete User [-d]\n")
    if command == "-n":
        AddUser()
    if command == "-d":
        DeleteUser()
    if command == "setup":
        SetUpDirectorys()
    return None

def AddUser():
    os.system("cls")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    username = hashlib.md5(username.encode()).hexdigest()
    password = hashlib.md5(password.encode()).hexdigest()
    line = "{\"username\":\""+username+"\";\"password\":\""+password+"\"}\n"
    with open(userDatabasePath, "a") as file:
        file.write(line)
        os.mkdir(storagePath+username)
    return None

def DeleteUser():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    deleteStoredData = input("Remove stored data? [y/n]")
    if deleteStoredData == "y":
        sure = input("Do you realy want to delte the user: " + username + " and the stored data ?[y/n]")
    if deleteStoredData == "n":    
        sure = input("Do you realy want to delte the user: " + username + "? [y/n]")
    if sure != "y":
        print("User not deleted. Returning.")
        Run()
    username = hashlib.md5(username.encode()).hexdigest()
    password = hashlib.md5(password.encode()).hexdigest()
    if CheckCredentials(username, password) == True:
        with open(userDatabasePath, "r") as file:
            lines = file.readlines()
        with open(userDatabasePath, "w") as file:
            for line in lines:
                if line.strip("\n") != "{\"username\":\""+username+"\";\"password\":\""+password+"\"}":
                    file.write(line)
        if deleteStoredData == "y":
            RemoveStoredData(username)
        return print("User removed from database and data deleted.")
    print("You entered a wrong username or password")

def RemoveStoredData(_username):
    fileList = os.listdir(storagePath + _username)
    for file in fileList:
        os.remove(storagePath+_username+"/"+file)
    os.rmdir(storagePath+_username)
    return None

def UserDataExists(_lines):
    for line in _lines:
        username, password = GetUserData(line)
        if username and password != "":
            return True
    return False

def CheckCredentials(_username, _password):
    with open (userDatabasePath, "r") as file:
        for line in file:
            username, password = GetUserData(line)
            if username == _username and password == _password:
                return True
    return False

def GetUserData(_line):
    if _line == None:
        return "",""
    result = re.search(pattern, _line)
    username = result.group(1)
    password = result.group(2)
    return username, password

def SetUpDirectorys():
    os.mkdir(os.getcwd()+"/static/Database")
    open(os.getcwd()+"/static/Database/userdatabase.db")
    os.mkdir(os.getcwd()+"/static/images")
    os.mkdir(os.getcwd()+"/static/STORAGE")
    Path(os.getcwd()+"/cloud.html").rename(os.getcwd()+"/templates/cloud.html")
    Path(os.getcwd()+"/login.html").rename(os.getcwd()+"/templates/login.html")
    Path(os.getcwd()+"/style.css").rename(os.getcwd()+"/static/style.css")
    Path(os.getcwd()+"/upload.js").rename(os.getcwd()+"/static/upload.js")

if __name__ == "__main__":
    Run()