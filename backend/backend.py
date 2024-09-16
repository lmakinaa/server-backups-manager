from flask import Flask, request
from datetime import datetime
from dotenv import load_dotenv
import tarfile
import dropbox
from ftplib import FTP
import itertools
import os


load_dotenv()

class BackupForger:
    def __init__(self, payload):
        self.backupStatus = "Successful"
        self.backupContent = payload["backupContent"]
        self.backupDest = payload["backupDest"]
        self.backupSchedule = payload["backupSchedule"]
        self.dropboxKey = payload["dropboxKey"]
        self.hostname = payload["host"]
        self.username = payload["username"]
        self.password = payload["password"]
        self.ftpPath = payload["ftpPath"]
        self.time = payload["time"]
        self.volumePath = os.getenv('VOLUMES_ROOT_PATH')
        self.outputFile = ""
        if self.backupContent != "all":
            self.volumePath += self.backupContent
    
    def compressVolume(self):
        self.outputFile = datetime.now().strftime("%d-%m-%y_%H-%M_%S-$f")[:-3] + self.backupContent + ".tar.gz"
        outputPath = "/tmp/" + self.outputFile
        with tarfile.open(outputPath, 'w:gz') as f:
            f.add(self.volumePath, arcname='')
        return outputPath

    def sendToDropbox(self, compressedFile):
        try:
            client = dropbox.Dropbox(self.dropboxKey)
            with open(compressedFile, 'rb') as f:
                client.files_upload(f.read(), "/" + self.outputFile)
            self.backupStatus = "Successful"
        except Exception as e:
            print(f"Failed to send to Dropbox: {e}")
            self.backupStatus = "Failed"

    def sendToFtp(self, compressedFile):
        try:
            with FTP(self.hostname, self.username, self.password) as ftp, open(compressedFile, 'rb') as f:
                print(f'STOR {self.ftpPath + "/" + self.outputFile}')
                ftp.storbinary(f'STOR {self.ftpPath + "/" + self.outputFile}', f)
            self.backupStatus = "Successful"
        except Exception as e:
            print(f"Failed to send to FTP: {e}")
            self.backupStatus = "Failed"

    def addToHistory(self):
        entry = f'Backup at {self.time} sent to {self.backupDest} has completed with status: {self.backupStatus}.\n'
        print(entry)
        with open(os.getenv('HISTORY_PATH'), 'a') as f:
            f.write(entry)
    


def getLastHistoryEntries():
    res = ""
    with open(os.getenv('HISTORY_PATH'), 'r') as f:
        for line in itertools.islice(f, 10):
            res += line.strip() + "\n"
    return res



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
    
    res.addToHistory()
    
    if res.backupStatus == "Failed":
        return "Backup failed", 400
    return "Backup Successful", 200


@app.route("/history")
def get_history():
    return getLastHistoryEntries()

if __name__ == "__main__":
    app.run(debug=True)
