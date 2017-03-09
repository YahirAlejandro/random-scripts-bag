import os
import subprocess
from datetime import datetime, timedelta

def cleanDate(date):
    clean = date.replace("-", "")
    return str(clean)

def execDirList(command):
    output = []
    process = subprocess.Popen(
        [command], stdout=subprocess.PIPE, shell=True
    )
    while True:
        line = process.stdout.readline()
        if line:
            line = line.rstrip()
            output.append(line)
        else:
            break
    return output

monitor_path = "/var/spool/asterisk/monitor/"
keep_days = 120
unkeeped_days = datetime.today() - timedelta(days=keep_days)

if __name__ == "__main__":
    date_to_delete = cleanDate(str(unkeeped_days)[:10])
    command = "ls " + monitor_path + "| grep " + date_to_delete
    recs_to_delete = execDirList(command)

    for rec in recs_to_delete:
        print "About to delete: " + rec
        os.remove(monitor_path + str(rec))
