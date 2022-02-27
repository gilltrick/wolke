from flask import Flask, make_response, render_template, request
import os, re, hashlib

app = Flask(__name__)
storagePath = os.getcwd() + "/static/STORAGE/"
userDatabasePath = os.getcwd() + "/static/Database/userdatabase.db"
pattern = re.compile("{\"username\":\"(.*)\";\"password\":\"(.*)\"}")
fileNamePattern = re.compile("<FileStorage:\s'(.*)'\s\('.*'\)")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    username = hashlib.md5(username.encode()).hexdigest()
    password = hashlib.md5(password.encode()).hexdigest()
    cookieValue = "{\"username\":\""+username+"\";\"password\":\""+password+"\"}"
    if CheckCredentials(username, password) == True:
        fileList, fileSizeList = GetData(username)
        response = make_response(render_template("cloud.html", fileList = fileList, fileSizeList = fileSizeList, username = username))
        response.set_cookie("data", cookieValue)
        return response
    return "<h1>wrong username or password</h1>"

@app.route("/cloud")
def cloud():
    cookieValue = request.cookies.get("data")
    username, password = GetUserData(cookieValue)
    if CheckCredentials(username, password) == True:
        fileList, fileSizeList = GetData(username)
        return render_template("cloud.html", fileList = fileList, fileSizeList = fileSizeList, username = username)
    return "<h1>Not allowed</h1>"

@app.route("/uploadFile", methods=["POST", "GET"])
def uploadFile():
    cookieValue = request.cookies.get("data")
    username, password = GetUserData(cookieValue)
    if CheckCredentials(username, password) == True:    
        file = request.files["fileToUpload"]
        fileName = GetFileName(str(file))
        if fileName == "":
            fileList, fileSizeList = GetData(username)
            return render_template("cloud.html", fileList = fileList, fileSizeList = fileSizeList, username = username)
        file.save(storagePath + username + "/" + fileName)
        fileList, fileSizeList = GetData(username)
    return "<h1>Not allowed</h1>"

@app.route("/deleteFile", methods=["POST"])
def deleteFile():
    cookieValue = request.cookies.get("data")
    username, password = GetUserData(cookieValue)
    if CheckCredentials(username, password) == True:
        fileName = request.form["fileName"]
        os.remove(storagePath + username + "/" + fileName)
        fileList, fileSizeList = GetData(username)
        return render_template("cloud.html", fileList = fileList, fileSizeList = fileSizeList, username=username)
    return "<h1>Not allowed</h1>"

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

def GetData(_username):
    fileList = os.listdir(storagePath + _username)
    fileSizeList = []
    for file in fileList:
        fileSizeList.append(GetFileSize(_username + "/" + file))
    return fileList, fileSizeList

def GetFileName(_file):
    result = re.search(fileNamePattern, _file)
    fileName = result.group(1)
    return fileName

def GetFileSize(_filePath):
    return os.stat(storagePath + _filePath).st_size

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5122)