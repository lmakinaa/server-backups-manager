from flask import Flask, jsonify, request
from datetime import datetime
import tarfile
import dropbox
from ftplib import FTP

class BackupForger:
    def __init__(self, payload):
        self.backupContent = payload["backupContent"]
        self.backupDest = payload["backupDest"]
        self.backupSchedule = payload["backupSchedule"]
        self.dropboxKey = payload["dropboxKey"]
        self.hostname = payload["host"]
        self.username = payload["username"]
        self.password = payload["password"]
        self.ftpPath = payload["ftpPath"]
        self.time = payload["time"]
        self.volumePath = "./data/"
        self.outputFile = ""
        if self.backupContent != "all":
            self.volumePath += self.backupContent

    def getData(self):
        print("backupContent:", self.backupContent)
        print("backupDest:", self.backupDest)
        print("backupSchedule:", self.backupSchedule)
        print("dropboxKey:", self.dropboxKey)
        print("host:", self.hostname)
        print("username:", self.username)
        print("password:", self.password)
        print("time:", self.time)
        print("volumePath:", self.volumePath)
        print("outputFile:", self.outputFile)
    
    def compressVolume(self):
        self.outputFile = datetime.now().strftime("%d-%m-%y_%H-%M_%S-$f")[:-3] + self.backupContent + ".tar.gz"
        outputPath = "/tmp/" + self.outputFile
        with tarfile.open(outputPath, 'w:gz') as f:
            f.add(self.volumePath, arcname='')
        return outputPath

    def sendToDropbox(self, compressedFile):
        client = dropbox.Dropbox(self.dropboxKey)
        with open(compressedFile, 'rb') as f:
            client.files_upload(f.read(), "/" + self.outputFile)

    def sendToFtp(self, compressedFile):
        with FTP(self.hostname, self.username, self.password) as ftp, open(compressedFile, 'rb') as f:
            print(f'STOR {self.ftpPath + "/" + self.outputFile}')
            ftp.storbinary(f'STOR {self.ftpPath + "/" + self.outputFile}', f)

    def makeBackup(self):
        compressedFile = self.compressVolume()
        if self.backupDest == "dropbox":
            print("Sending to dropbox has been started..")
            self.sendToDropbox(compressedFile)
        elif self.backupDest == "ftp":
            self.sendToFtp()





app = Flask(__name__)
@app.route("/start-backup", methods=["POST"])
def do_backup():
    res = BackupForger(request.json)
    compressedFile = res.compressVolume()

    if res.backupDest == "dropbox":
        print("Sending to dropbox has been started..")
        res.sendToDropbox(compressedFile)
    elif res.backupDest == "ftp":
        print("Sending to ftp has been started..")
        res.sendToFtp(compressedFile)

    return {"status": 200}

if __name__ == "__main__":
    app.run(debug=True)
