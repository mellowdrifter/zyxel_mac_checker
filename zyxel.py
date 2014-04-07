import cookielib
import urllib
import urllib2
import re

devices=[]
try:
    with open('devices.dsl') as file:
        pass
except IOError as e:
    print"\ndevices.txt does not exist or unreadable, exiting now"
    exit()

f = open('devices.dsl')
for line in f:
    devices.append(line.rstrip())

try:
    with open('report.txt') as file:
        choice = raw_input("\nreport.txt already exists. Do you want to overwrite it? [y/n]: ")
        while choice not in ["y","n"]:
            choice = raw_input("Invalid choice! Do you want to overwrite report.txt? [y/n]: ")
        if choice == "n":
            print"\nExiting now"
            exit()
        else:
            print"\nreport.txt will be overwritten!"
            f = open('report.txt', 'w')
            f.close()
except IOError as e:
    pass

#Change this to match your own hashed password
hashed = 'o6DrESL67Yozzt43oBhe'
    
for device in devices:
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Newscript')]
    urllib2.install_opener(opener)
    authentication_url = 'http://'+device+'/Forms/rpAuth_1'
    payload = {'LoginPassword': 'ZyXEL\+ZyWALL\+Series','hiddenPassword':hashed,'Prestige_Login':'Login'}
    data = urllib.urlencode(payload)
    req = urllib2.Request(authentication_url, data)
    f = open('report.txt', 'a')
    try:
        resp = urllib2.urlopen(req,timeout=3)
        response = urllib2.urlopen('http://'+device+'/home.html',timeout=2)
        html = response.read()
        output = re.split(r'[;,\s,<]\s*', html)
        print "\n\n\n"+device+" :"
        f.write("\n\n\n"+device+" :\n")
        for i in output:
            m = re.search(r'([a-fA-F0-9]{2}[:]?){6}', i)
            if m:
                print "MAC Address :\t", m.group()
                f.write("MAC Address :\t" +str(m.group())+"\n")
            if "cad" in i:
                print "Hostname is :\t", i
                f.write("Hostname is :\t" +str(i)+"\n")
    except urllib2.URLError:
        print "\n\nUnable to resolve or log into",device,"- Does it exist?"
        f.write("\n\nUnable to resolve or log into "+str(device)+" - Does it exist?")
    f.close()
