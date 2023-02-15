import socket
import sys
import time
import subprocess

from subprocess import Popen, CREATE_NEW_CONSOLE
stoppingSw=1

slowdown=False
testPerf=True
PerfCounter=0
lastId=0
oldTime=newTime = time.perf_counter()
class commCpp ():
    def __init__(self):#, threadID, name, countertmpCmd
        # self.name = name
        # self.counter = counter
        self.running=False
        self.StsInternal=0
        self.stopSub=False
        self.DataOutContainer=[]
        self.DataInContainer=[]
        self.started=False
        self.performance=0
        self.startSeq()
        self.callProcess



    def setupy(self):
        #Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5555)
        aa=sys.stderr

        print(  'connecting to %s port %s' % server_address)

        self.sock.connect(server_address)
        self.sock.setblocking(False)



    def startSub(self):
        self.callProcess = subprocess.Popen(['C:/PyPj/doublepend2/build/Release/doublepend2.exe', '-l'], creationflags=CREATE_NEW_CONSOLE)
        print(self.callProcess)


    def startSeq(self):
        self.running=True
        time.sleep(1)
        self.startSub()
        time.sleep(4)
        self.setupy()



    def runningf(self,newItem, DataOut, endProg):
        global lastId
        DataIn=[0,0,0,0,0,0,0,0,0,0]



        cmdInternal=0

        data=[]


        if(endProg):
            print("endprog --------------------------------------------------")
            self.running=False
#            os.kill(self.callProcess.pid, signal.CTRL_BREAK_EVENT)  # Send the signal to all the process groups
            subprocess.call(['taskkill', '/F', '/T', '/PID',  str(self.callProcess.pid)])
            self.sock.close()
            return False, False
            
        if (not self.running):
            time.sleep(0.2)  

            
            if(newItem):
                cmdInternal=DataOut[0]
                if(cmdInternal==1):
                    self.stopSub=True                
            print("not running")
            return False, False

        #while (self.running):
            
        a_converted = ""
        
        

#----------------------------sender til cpp-------------------------------------
        # dataOut[0]=cmd
        # dataOut[1]=self.M1ActCommand
        # dataOut[2]=self.M2ActCommand
        # dataOut[3]=self.ActTimeVal1
        # dataOut[4]=self.ActTimeVal2
        # dataOut[5]=self.IDout
        
        if(newItem):
           # print("newitem")



            integer_val = DataOut[0]
            cmdInternal=DataOut[0]

            if(cmdInternal==1):
                self.stopSub=True
            integer_val2=0

            bytey =  integer_val.to_bytes(1,  byteorder='big',signed=False)

            bytey +=  integer_val2.to_bytes(1,  byteorder='big',signed=False)

            for i in range(1, 7):#1,2,3
                integer_val = DataOut[i] & 0xFF
                integer_val2 = DataOut[i] >> 8
                
                bytey +=  integer_val.to_bytes(1,  byteorder='big',signed=False)
                bytey +=  integer_val2.to_bytes(1,  byteorder='big',signed=False)


            

            if (not self.stopSub):
                try:
                    bb=self.sock.send(bytey)
                except BlockingIOError:
                    print("# This error is raised if the socket is in non-blocking mode and no data is available to send")

                    return   False, False                          
                except Exception as ex:
                    template = "yo!! An exception of type {0} occurred. Argumentiados:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print (message)
                    self.running=False
                    return False, False
            else:
                #if(self.stopSub):
                a_converted = "a"
                bytey=(a_converted.encode()) 
                try:
                    self.sock.send(bytey)
                except BlockingIOError:
                    print("# This error is raised if the socket is in non-blocking mode and no data is available to be read")

                    return False, False
                except Exception as ex:
                    template = "yo!! An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print (message)
                    self.running=False
                    #break
                    return False, False

            #if(self.stopSub):




#----------------------------mottar fra cpp-------------------------------------

            # self.v1=IntTypefloat16_to_float32(DataIn[1])
            # self.v2=IntTypefloat16_to_float32(DataIn[2])
            # self.AVst=IntTypefloat16_to_float32(DataIn[3])
            # self.DeltaV1=IntTypefloat16_to_float32(DataIn[4])
            # self.DeltaV2=IntTypefloat16_to_float32(DataIn[5])
            # self.DeltaVAvst=IntTypefloat16_to_float32(DataIn[6])
            # self.IncomID=DataIn[7]

        #//0 sts, 1 v1, 2 v2,3 avst, 4 dv1, 5 dv2, 6 dvAvst, 7 id
        try:
            data=self.sock.recv(16)
        except BlockingIOError:
            # This error is raised if the socket is in non-blocking mode and no data is available to be read
            return False, False
            
        # if(len(read_ready)>0):
        #     try:
            
        #         data=self.sock.recv(14)
                
        except Exception as ex:
            template = "yo!! An exception of type {0} occurred. Arguments sjoe:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message) 
            self.running=False

            return False, False
            

        
        if(len(data)>15):

            for i in range(8):
                DataIn[i]=data[i*2+1]*256+data[i*2]

            lastId=DataIn[7]

            if(self.stopSub):
                DataIn[0]=1
            self.StsInternal=DataIn[0]
        
            
            #print(DataIn)
            return True, DataIn
                
        else:
            print("kort: " + str(len(data)>15))
            return False, False

    

