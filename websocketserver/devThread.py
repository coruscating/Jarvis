import threading
import traceback
import socket
import struct
import ast, json
import errno
import time

from pymongo import MongoClient


############# MongoDB #############
client = MongoClient('quanta-rabi')
db = client.jarvis

class devThread(threading.Thread):
    def __init__(self,socketobj, devname, server):
        threading.Thread.__init__(self)
        self.client = socketobj
        self.running = 1
        self.server = server
        self.devname = devname
        self.errors = 0
        self.counter = 0
        self.packetsize = 25000 # above this size, messages are split up and sent packet by packet
    # Listen to messages from the client and forward them
    # to the worker thread when they arrive
    def run(self):
        while self.running:
            try:
                data = self.recvMessage()
                if data:
                    # Sample input
                    # STATUS 1407784757.2 {1033: 'OPEN', 1092: 'OPEN', 405: 'CLOSE', 422: 'CLOSE', 461: 'CLOSE'}
                    # Change to
                    # STATUS;1407784757.2;Shutters;{1033: "OPEN", 1092: "OPEN", 405: "CLOSE", 422: "CLOSE", 461: "CLOSE'}
                    self.server.debugMsg("Device " + self.devname + " sent data: " + data)
                    data = data.rstrip("\n\r")
                    data2 = data.split(" ", 2)

                    self.server.current_states.update(ast.literal_eval(data2[2])) # update dictionary with new data
                    #print self.devname + " " + str(self.server.current_states["SourceMeterVolt"])
                    header = data2[0] + ";" + data2[1] + ";" + self.devname + ";"
                    payload = json.dumps(ast.literal_eval(data2[2]))

                    message = header + payload # Send dictionary in JSON format (double quotes)

                    if data2[0].startswith("PLOTSCRIPT"): # let the scriptThread handle this
                        plotid=data2[0].split("-")
                        # have to get rid of the pesky prefix
                        plotid=plotid[0].replace("PLOTSCRIPTHEAT","")
                        plotid=plotid.replace("PLOTSCRIPT2D","")
                        plotid=plotid.replace("PLOTSCRIPT", "")
                        if plotid in self.server.scriptdict:
                            self.server.scriptdict[plotid].sendplot(data2[0],data2[1],self.devname,ast.literal_eval(data2[2])) # hand over to plotThread                      
                    elif data2[0].startswith("PLOT"): # let the plotThread handle this
                        plotid=data2[0].split("-")
                        # have to get rid of the pesky prefix
                        plotid=plotid[0].replace("PLOTHEAT","")
                        plotid=plotid.replace("PLOT2D","")
                        plotid=plotid.replace("PLOT", "")
                        if plotid in self.server.plotdict: # if this is one of our plots
                            self.server.plotdict[plotid].sendplot(data2[0],data2[1],self.devname,ast.literal_eval(data2[2])) # hand over to plotThread
                    elif data2[0].startswith("SPECIALREQUESTSCRIPT"): # ddscon scripts
                        plotid=data2[0].replace("SPECIALREQUESTSCRIPT","")
                        if plotid in self.server.scriptdict:
                            self.server.scriptdict[plotid].sendddsconplot(message)
                    else:
                        self.counter += 1
                        if self.counter == 3600:
                            db.update.insert_one(
                                        {"time":time.time(),"device": self.devname,"variables":ast.literal_eval(data2[2])}
                                        )
                            self.counter = 0
                        if len(self.server.webthreads) != 0:
                            if len(payload) + len(header) > self.packetsize:
                                chunksize=self.packetsize-len(header) # max size of payload in each packet
                                chunknum=len(payload)//chunksize+1 
                                if len(payload)%chunksize == 0: # if payload length evenly divides chunksize then we have overcounted number of chunks by one
                                    chunknum-=1
                                #for i in range(0, len(payload), chunksize):
                                #    print header + str(i/chunksize) + ";" + str(chunknum) + ";"

                                # break the message into chunks and assemble with header
                                # format is HEADER;packet number;total packet number;PAYLOAD
                                messages=[header + str(i/chunksize) + ";" + str(chunknum) + ";" + payload[i:i+chunksize] for i in range(0, len(payload), chunksize)]

                                # send to websocket
                                for submsg in messages:
                                    self.server.webQueue.put(submsg)
                            else:
                                self.server.webQueue.put(message)

                    self.errors=0 # reset errors if working
            except Exception as e:
                self.errors+=1
                self.server.debugMsg("Receive error from %s: %s. Error #%d" %(self.devname, str(e),self.errors))
                print traceback.format_exc()
                if self.errors>=10:
                    self.kill()

    def recvMessage(self):
        # unpack TCP frames
        # see http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = self.client.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    
    # Send a given message to the client socket    
    def sendMessage(self, message):
        try:
            self.client.send(message + '\n')

        except socket.error, e:
            print "ERROR: Socket invalidated while sending"
            print traceback.format_exc()
            self.kill()

    def kill(self):
        print "%s device being killed" %(self.devname)
        if self.running == 1:
            self.running = 0

            try:
                self.server.debugMsg("Killing the dev client connection")
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                
            except socket.error, e:
                if isinstance(e.args, tuple):
                    if e[0] == errno.ENOTCONN:
                        self.server.debugMsg("Closing the socket failed (Socket already closed)")
                    else:
                        self.server.debugMsg(str(e.args))
                else:
                    self.server.debugMsg("Error while closing the client connection: " + str(e))
                print traceback.format_exc()

            finally:
                # delete thread and delete from active device dictionary
                self.server.removeClient(self, 'dev')
                self.server.devdict.pop(self.devname, False)
                self.server.webQueue.put("DELCONN;" + self.devname)



