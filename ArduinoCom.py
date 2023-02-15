
from pymodbus.client.sync_diag import ModbusTcpClient as ModbusClient


from multiprocessing import Process, Queue
import time


def modbus(output_queue,input_queue):

    testcounterd=0
    oldTimed=newTimed = time.perf_counter()
    class modbusc:
        def __init__(self):
            self.client = ModbusClient('192.168.100.177')
            self.connected=True

        def setupComm(self):
            success=True
            try:
                (self.client.connect)
            except:
                success=False

            try:
                self.client.read_holding_registers(0, 3 , slave=1)
            except:
                success=False

            return(success)
        def MoveCommand(self, commands):

            rq = self.client.write_registers(0, commands , slave=1)
            return(rq.function_code < 0x80)     # test that we are not an error. true ok, false er feil

    mb1=modbusc()

    success=mb1.setupComm()
    testval=0
    hzVal=0
    while(True):
        if(input_queue.empty()):
            continue
        else:   
            testcounterd+=1
            newTimed = time.perf_counter()
            deltaTimed=newTimed-oldTimed            
            if(deltaTimed>1):
                oldTimed=newTimed = time.perf_counter()

                hzVal=testcounterd
                testcounterd=0


            DataOut=input_queue.get()
            cmd=DataOut[0]
            #if(DataOut[1]>11):
           #     print(f"ard commsy {DataOut}")
            # testval=DataOut[1]
            if(cmd==1):
                print("ard cmd stop2")
                mb1.client.close()
                break

            result=mb1.MoveCommand(DataOut)

        output_queue.put([True,hzVal,result])
    print("modbus avsluttet")






class ArdComm: 
    def __init__(self):
        self.reggy=[]
       # self.client = ModbusClient('192.168.100.177')
        self.connected=True
        self.DataInContainer=[]
        self.DataOutContainer=[]
        self.cmd=0
        self.stopping=False
        self.qOut = Queue()
        self.qIn = Queue()
        self.testval=0
        self.testCounter=0

        self.hzVal=0
        self.oldTime=self.newTime = time.perf_counter()
        self.Extprocess()        


    def Extprocess(self):
        self.p1 = Process(target=modbus, args=(self.qIn, self.qOut))
        print("vi er i gang____________________________")
        self.p1.start()

    def MoveCommand(self, commands): 

        #print(commands)
        # if(commands[1]>10):
        #     print(f"ard commsy hei hei [{commands}")
        # if(self.qIn.qsize()>0):
        #     result=self.qIn.get()
                #print(result)
        self.qOut.put(commands)

        if(not(self.qIn.empty())):
            res=(self.qIn.get())
            self.hzVal=res[1]
        # time.sleep(0.01)
        # print(self.qIn.get())

    def shutDown(self):
        self.qOut.put([1,0,0,0,0])
        print("ard shut down1")


    def running(self,DataOut):
        
        newItem=DataOut[5]
        # if(self.testval != DataOut[1]):
        #     print(f"ard commsy 111 {DataOut}")
        # self.testval=DataOut[1]


        DataIn=[0,0]
        TmtCount=0
        
        


        #while(True):
            #time.sleep(0.00001)
        
        self.newTime = time.perf_counter()
        deltaTime=self.newTime-self.oldTime            
        if(deltaTime>1):
            self.oldTime=self.newTime = time.perf_counter()
            secFlag=True
            # print(f"Hz ard hoved: {self.testCounter}")

            # print(f"Hz ard: {self.hzVal}")
            self.testCounter=0


        #newItem,DataOut=CommonFunc.popFirst(self.DataOutContainer)
        if(newItem):   #outgoing main->ard_th->ard
            self.testCounter+=1
            newItem=False
            self.cmd=DataOut[0]
            # print("ard cmd herherherherher")
           

            #print(DataOut)
            self.MoveCommand(DataOut)

            result=True
            if(self.cmd==1):
                print("ard cmd stop")
                self.stopping=True                
            TmtCount+=1
        else:
            return

        #self.MoveCommand(self, DataIn)

        if(not(result)):#
            DataIn[0]+=1 #error counter

        if(TmtCount>30 or self.stopping):
            TmtCount=0
            
            if(self.stopping):
                DataIn[1]=1

            #CommonFunc.PushLast(DataIn,self.DataInContainer)
        
        if(self.stopping):
            
            return


