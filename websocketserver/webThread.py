import threading
import traceback
import socket
import struct
import ast, json
import errno
import time

from subprocess import call
from pymongo import MongoClient
# websocket modules
from base64 import b64encode
from hashlib import sha1
from mimetools import Message
from StringIO import StringIO

from plotThread import plotThread
from scriptThread import scriptThread
from lockThread import lockThread

############# MongoDB #############
client = MongoClient('quanta-rabi')
db = client.jarvis

# class for threads with web gui, listens to commands from web GUI

class webThread(threading.Thread):
    def __init__(self,(client,address), server):
        threading.Thread.__init__(self)

        self.server = server
        self.client = client
        self.client.settimeout(2)
        self.address = address
        self.running = 1
        self.magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        self.handshake_done = False
        self.errors = 0 # keeps count of errors
        self.buffer = ""
    
    # Listen to messages from the client and forward them
    # to the worker thread when they arrive
    def run(self):
        while self.running:
            if not self.handshake_done:
                self.handshake()
                if self.handshake_done:
                    pass
                    #self.server.webQueue.put("SERVERSTATUS;" + str(len(self.server.webthreads)) + ";" + str(len(self.server.devthreads)) + ";" + str(len(self.server.plotthreads)) + ";" + str(len(self.server.scriptthreads)) + ";" + str(len(self.server.lockthreads)))
            else:
                try:
                    # read the next message
                    try:
                        data = self.client.recv(9000)
                    except: # nothing from client, just keep listening
                        continue
                    #print "data=" + ':'.join(x.encode('hex') for x in data)
                    self.buffer += data
                    i=0
                    while len(self.buffer)>2:            
                        message=self.parse_frame()
                    
                        if message is not None and isinstance(message, basestring):
                            if len(message)>3:
                                print message
                                parsedmsg = message.split(";")
                            
                                if parsedmsg[0] == "SET": # setting something
                                    # SET;Shutters;OPEN 405 
                                    self.server.devQueue.put(message.replace('SET;',''))
                                    # mongo: insert into set {"time": timestamp, "device": Shutters, "io": "OPEN", "value": "405"}
                                    global db
                                    db.set.insert_one(
                                        {"timestamp":time.time(),"device": parsedmsg[1],"io":parsedmsg[2].split(" ")[0], "value":parsedmsg[2].split(" ")[1]}
                                        )
                                elif parsedmsg[0] == "SERVERSTATUS":
                                    self.server.webQueue.put("SERVERSTATUS;" + str(len(self.server.webthreads)) + ";" + str(len(self.server.devthreads)) + ";" + str(len(self.server.plotthreads)) + ";" + str(len(self.server.scriptthreads)) + ";" + str(len(self.server.lockthreads)))
                                elif parsedmsg[0] == "SPEAKLOG":
                                    self.server.webQueue.put("SPEAKLOG;" + json.dumps(list(self.server.speaklog)))
                                elif parsedmsg[0] == "PLOT":
                                    newplotThread = plotThread(self.server, message)
                                    newplotThread.start()
                                    self.server.plotthreads.append(newplotThread)
                                elif parsedmsg[0] == "STOPPLOT":
                                    self.server.delPlot(parsedmsg[1])
                                elif parsedmsg[0] == "PAUSEPLOT":
                                    self.server.pausePlot(parsedmsg[1])
                                elif parsedmsg[0] == "SCRIPT":
                                    newscriptThread = scriptThread(self.server, message)
                                    newscriptThread.start()
                                    self.server.scriptthreads.append(newscriptThread)
                                elif parsedmsg[0] == "STOPSCRIPT":
                                    self.server.delScript(parsedmsg[1])
                                elif parsedmsg[0] == "RUN": # run screenshot-to-blog script
                                    print ''.join(parsedmsg[1:])
                                    call(''.join(parsedmsg[1:]))
                                elif parsedmsg[0] == "LOCK":
                                    newlockThread = lockThread(self.server, message)
                                    newlockThread.start()
                                    self.server.lockthreads.append(newlockThread)
                                elif parsedmsg[0] == "LOCKUPDATE":
                                    lockid=parsedmsg[1]
                                    self.server.lockdict[lockid].updateParams(message)
                                elif parsedmsg[0] == "UNLOCK":
                                    self.server.unLock(parsedmsg[1]);
                                elif parsedmsg[0] == "ADDCONN": # connect to device
                                    if self.server.addConnDev(parsedmsg[1]): #success
                                        self.server.webQueue.put("ADDCONN;" + parsedmsg[1]);
                                elif parsedmsg[0] == "DELCONN": # disconnect from device
                                    if self.server.delConnDev(parsedmsg[1]):
                                        self.server.webQueue.put("DELCONN;" + parsedmsg[1]);
                                elif parsedmsg[0] == "CONNLIST": # list connected devices
                                    self.server.webQueue.put("CONNLIST;" + json.dumps(ast.literal_eval(str([str(x) for x in self.server.devdict.keys()]))))
                                elif parsedmsg[0] == "RELOAD":
                                    self.server.IOMap = json.load(open(IOMAP_FILE))
                                    self.server.devices = json.load(open(DICT_FILE))
                                elif parsedmsg[0] == "CLOSE":
                                    self.kill()
                                
                                self.errors=0 # reset errors if working
                        i+=1
                        if i>5: # try to read again
                            self.buffer=""
                            break
                    
                except Exception as e:
                    print("Reading from web client failed: " + str(e))
                    print traceback.format_exc()
                    self.errors+=1
                    if self.errors >= 10:
                        print("Too many errors from web client, quitting")
                        self.kill()
                        break


    def handshake(self): 
        try:
            data = self.client.recv(1024).strip()
            headers = Message(StringIO(data.split('\r\n', 1)[1]))
            if headers.get("Upgrade", None) != "websocket":
                return
            print 'Handshaking with web application...'
            key = headers['Sec-WebSocket-Key']
            digest = b64encode(sha1(key + self.magic).hexdigest().decode('hex'))
            response = 'HTTP/1.1 101 Switching Protocols\r\n'
            response += 'Upgrade: websocket\r\n'
            response += 'Connection: Upgrade\r\n'
            response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
            self.client.send(response)
            
            # Have to make sure the handshake is successful before we add 
            # it as a client thread or it will get lots of data dumps before
            # connection is ready. Doing it here so it doesn't hold up the main thread.
            
            self.server.serverLock.acquire()
            self.server.webthreads.append(self)
            self.server.serverLock.release()
            
            print "added thread"
            self.handshake_done = "websocket"
        except Exception as e:
            print "Error in handshake: %s" %(str(e))
            print traceback.format_exc()
            self.kill()
    
    def sendMessage(self, message):
        #self.server.debugMsg("sending websocket message %s" %(message))
        length = len(message)
        self.server.debugMsg("sending websocket message length=%d"%(length)) 
        try:
            self.client.send(chr(129))
            if length <= 125:
                self.client.send(chr(length))
            elif length >= 126 and length <= 65535:
                self.client.send(chr(126))
                self.client.send(struct.pack(">H", length))
            else:
                self.client.send(chr(127))
                self.client.send(struct.pack(">Q", length))
            self.client.send(message)
            self.errors=0
        except Exception as e:
            self.server.debugMsg("Sending to web client failed: %s" %(e))
            print traceback.format_exc()
            self.errors+=1
            if self.errors >= 10:
                self.kill()

    

    def parse_frame(self):
        try:
            # Parse a WebSocket frame. If there is not a complete frame in the
            # buffer, return without modifying the buffer.   
            buf = self.buffer       
            payload_start = 2

            # try to pull first two bytes
            if len(buf) < 3:
                return
            b = ord(buf[0])
            fin = b & 0x80      # 1st bit
            # next 3 bits reserved
            opcode = b & 0x0f   # low 4 bits
            b2 = ord(buf[1])
            mask = b2 & 0x80    # high bit of the second byte
            length = b2 & 0x7f    # low 7 bits of the second byte

            # check that enough bytes remain
            if len(buf) < payload_start + 4:
                print "Jarvis read: not enough bytes"
                return
            elif length == 126:
                length, = struct.unpack(">H", buf[2:4])
                payload_start += 2
            elif length == 127:
                length, = struct.unpack(">I", buf[2:6])
                payload_start += 4

            if mask:
                mask_bytes = [ord(b) for b in buf[payload_start:payload_start + 4]]
                payload_start += 4

            # is there a complete frame in the buffer?
            if len(buf) < payload_start + length:
                print "Jarvis read: not complete frame"
                return

            # remove leading bytes, decode if necessary, dispatch
            payload = buf[payload_start:payload_start + length]
            self.buffer = buf[payload_start + length:]

            # use xor and mask bytes to unmask data
            if mask:
                unmasked = [mask_bytes[i % 4] ^ ord(b)
                                for b, i in zip(payload, range(len(payload)))]
                payload = "".join([chr(c) for c in unmasked])

            if opcode == 0x01:
                s = payload.decode("UTF8")
                return(s)
            if opcode == 0x02:
                return(payload)
            return True
        except Exception as e:
            self.server.debugMsg("Sending to web client failed: %s" %(e))
            print traceback.format_exc()
            return

      
    def kill(self):
        if self.running == 1:
            self.running = 0

            try:
                self.server.debugMsg("Killing the web client connection")
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
            
            except socket.error, e:
                if isinstance(e.args, tuple):
                    if e[0] == errno.ENOTCONN:
                        self.server.debugMsg("Closing the socket failed (Socket already closed)")
                    else:
                        self.server.debugMsg(str(e.args))
                else:
                    self.debugMsg("Error while closing the client connection: " + str(e))
                print traceback.format_exc()

            finally:
                self.server.removeClient(self, 'web')



