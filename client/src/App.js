import { useState } from 'react'


function getCurrentDateTime() {
  const date = new Date();
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // January is 0!
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}-${month}-${year} ${hours}:${minutes}`;
}

function App() {
  const [backupStatus, setBackupStatus] = useState(0);
  const [backupContent, setBackupContent] = useState("");
  const [backupDest, setBackupDest] = useState("");
  const [backupSchedule, setBackupSchedule] = useState("");
  
  const [googleApiKey, setGoogleApiKey] = useState("");

  const [host, setHost] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleBackupSchedule = (e) => {
    console.log(e.target.value);
    setBackupSchedule(e.target.value);
  }


  const handleBackupChange = (e) => {
    console.log(e.target.value);
    setBackupContent(e.target.value);
  }

  const handleBackupDest = (e) => {
    console.log(e.target.value);
    setBackupDest(e.target.value);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setBackupStatus(1);
  
    await fetch("/start-backup", {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        backupContent: backupContent,
        backupDest: backupDest,
        backupSchedule: backupSchedule,
        host: host,
        username: username,
        password: password,
        time: getCurrentDateTime(),
      }),
    }).then(
      res => res.json()
    ).then(
      data => {
        console.log(data);
      }
    )
    setBackupStatus(2);
  }

  return (
    <>
      <div className='flex items-center justify-center'>
        <h1 className="text-4xl font-bold m-9 text-center custom-text-blue">
          Server Backups Manager
        </h1>
      </div>
      <div className='p-6'>
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-8'>
          <form action="" onSubmit={handleSubmit}>
            <div className="custom-bg-dark p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-4 custom-text-blue">
                Create Backup
              </h2>
              <div className="mb-4">
                <h3 className="text-xl mb-2">
                  Backup Content
                </h3>
                <ul className="space-y-2">
                  <li>
                    <label className="inline-flex items-center cursor-pointer">
                      <input value="all" type="radio" name="backup-content" className="custom-checkbox" onChange={handleBackupChange} />
                      <span className="ml-2">All</span></label>
                  </li>
                  <li>
                    <label className="inline-flex items-center cursor-pointer">
                      <input value="wordpress" type="radio" name="backup-content" className="custom-checkbox" onChange={handleBackupChange} />
                      <span className="ml-2">WordPress Files only</span>
                    </label>
                  </li>
                  <li>
                    <label className="inline-flex items-center cursor-pointer">
                      <input value="database" type="radio" name="backup-content" className="custom-checkbox" onChange={handleBackupChange} />
                      <span className="ml-2">Database only</span>
                    </label>
                  </li>
                </ul>
              </div>
              <div className="mb-4">
                <h3 className="text-xl mb-2">Destination</h3>
                <select className="custom-select w-full" onChange={handleBackupDest}>
                  <option value="google-drive">Google Drive</option>
                  <option value="ftp">FTP Server</option>
                </select>
                {backupDest === "ftp" ?
                <div>
                  <input
                    type="text"
                    placeholder='Host..'
                    name="ftp-server"
                    className="mt-2 custom-text w-full"
                    value={host}
                    onChange={(e) => setHost(e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder='Username..'
                    name="ftp-server"
                    className="mt-2 custom-text w-full"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                  <input
                    type="password"
                    placeholder='Password..'
                    name="ftp-server"
                    className="mt-2 custom-text w-full"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
                : <div><input
                    type="text"
                    placeholder='Api Key..'
                    name="google-api-key"
                    className="mt-2 custom-text w-full"
                    value={googleApiKey}
                    onChange={(e) => setGoogleApiKey(e.target.value)}
                  /></div>}
              </div>
              <div className="mb-4">
                <h3 className="text-xl mb-2">Schedule</h3>
                <select className="custom-select w-full" onChange={handleBackupSchedule}>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
              <button className="custom-button w-full">Start Backup</button>
            </div>
          </form>
          <div className="space-y-8">
            <div className="custom-bg-dark p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-4 custom-text-blue">Backup History</h2>
              <p>No backup history available.</p>
            </div>
            <div className="custom-bg-dark p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-4 custom-text-blue">Console Log</h2>
              <div className="bg-black text-green-400 p-4 rounded font-mono" style={{ whiteSpace: 'pre-line' }}>
                {backupStatus === 0
                  ? "No console logs available."
                  : (backupStatus === 1
                    ? "Backup started..."
                    : "Backup started...\nBackup finished!")
                }
              </div>
            </div>
          </div>
        </div>
      </div>
    </>

  )
}

export default App
