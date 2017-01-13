import time, os, sys, ftplib

def validFiles(path):
    """Checks and yields valid Asterisk files on given path at current time."""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if str(file).find(timeDirs[0:4] +  timeDirs[4:6] +  timeDirs[6:8] + "-" +  timeDirs[8:10]) != -1:
                yield file

def createRemoteDir(nextDir):
    """Creates remote FTP directory structure."""
    try:
        print "Will try to move to %s" % nextDir
        ftpSession.cwd(str(nextDir))
    except ftplib.error_perm, resp:
        if str(resp)[0:3] == "550":
            print "550 no directory called %s, will create it" % nextDir
            ftpSession.mkd(str(nextDir))
        print "It's created, now will move"
        ftpSession.cwd(str(nextDir))
        print "Now in" + ftpSession.pwd()

def flagCheck(flag):
    """Check flags passed to script.

    Valid arguments are:
        "-a": Regular Asterisk monitor directory, with no subdirectories.
        "-e": Elastix >4 monitor directory, with subdirectories.
    """
    if flag == '-a':
        monitorPath = "/var/spool/asterisk/monitor/"
        return monitorPath
    elif flag == '-e':
        monitorPath = "/var/spool/asterisk/monitor/%s" % time.strftime('%Y/%m/%d')
        return monitorPath

timeDirs = time.strftime('%Y%m%d%H')
remotePath = ['/home', 'ftpaudiobackup', timeDirs[0:4], timeDirs[4:6], timeDirs[6:8], timeDirs [8:10]]

if __name__ == "__main__":
    ftpSession = ftplib.FTP('nsftp.ftp.com', 'user', 'password')

    for directory in remotePath:
        createRemoteDir(directory)

    monitorPath = flagCheck(sys.argv[1])

    for file in validFiles(monitorPath):
        storCommand = "STOR %s" % str(file)

        try:
            print "Will try to locate %s in %s" % (str(file), ftpSession.pwd())
            checkRemoteFile = ftpSession.nlst(str(file))
            ftpResp = ""
            print checkRemoteFile
        except ftplib.error_perm, resp:
            ftpResp = str(resp)[0:3]
        if ftpResp == "550" or not checkRemoteFile:
            print "%s was not found, will upload it" % str(file)
            localPathFile = "%s/%s" % (str(monitorPath), str(file))
            fileToUpload = open(localPathFile, 'rb')
            ftpSession.storbinary(storCommand, fileToUpload)
            fileToUpload.close()
            print "Uploaded %s" % str(file)
    print "Finished."
    ftpSession.quit()
