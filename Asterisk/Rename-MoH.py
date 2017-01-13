import os

mohPath = "/var/lib/asterisk/mohmp3/"

for filename in os.listdir(mohPath):
    if filename.endswith("bak"):
        print "%s is correctly renamed." % filename
    else:
        filename = os.path.join(mohPath, filename)
        os.rename(filename, filename + ".bak")
        print "Changed %s to bak." % filename
