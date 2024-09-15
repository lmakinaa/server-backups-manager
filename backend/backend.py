from flask import Flask, jsonify, request

class BackupForger:
    def __init__(self, payload):
        self.backupContent = payload["backupContent"]
        self.backupDest = payload["backupDest"]
        self.backupSchedule = payload["backupSchedule"]
        self.host = payload["host"]
        self.username = payload["username"]
        self.password = payload["password"]
        self.time = payload["time"]

    def getData(self):
        print("backupContent:", self.backupContent)
        print("backupDest:", self.backupDest)
        print("backupSchedule:", self.backupSchedule)
        print("host:", self.host)
        print("username:", self.username)
        print("password:", self.password)
        print("time:", self.time)
    
    def makeBackup:
        dataPath = "/home/ijaija/data"




app = Flask(__name__)
@app.route("/start-backup", methods=["POST"])
def do_backup():
    res = BackupForger(request.json)
    res.getData()
    
    return {"item": ["22:00"]}

if __name__ == "__main__":
    app.run(debug=True)


#@app.route("/", methods=['Get'])
#def main_uri():
#    return "<p>Hello, World!</p>"
