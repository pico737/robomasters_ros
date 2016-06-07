#from subprocess import Popen, PIPE, STDOUT
import subprocess
import time

cmd = ["stdbuf", "-oL", "rosrun", "rm_cv","ZED_PROJECT"]
#cmd = ["stdbuf", "-oL", "./test"]

#p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)


#process stdout to store cv info
while p.poll() is None:
    #line = p.stdout.readline()
    #print "post line" + line.rstrip()

    line = p.stdout.readline()
    if line != "" and "ZED" not in line:
        #print "post if line" + line.rstrip()
        x_center,y_center,distance = line.split(", ")
        #print x_center + "; " + y_center + "; " + distance
        if(int(x_center) == 0):
            print "HELLO"


#while(1 == 1):
#    line = p.stdout.readline()
#    if line != "" and "ZED" not in line:
#        print "post if line" + line.rstrip()
#        #x_center,y_center,distance = line.split(", ")
#        #if(x_center == 0):
#        #    print "HELLO"
