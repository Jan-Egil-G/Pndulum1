from statistics import stdev

import torch


from collections import deque
from y_model import NeuralNetCtrl
from torch.multiprocessing import Process, Queue
import sys
import time
import math
def linearInterpolation(x1, x2,  y1,y2, x):
    return y1 + (x - x1) * ((y2 - y1) / (x2 - x1))
def twosComplement(inputValue, numBits):
    mask = 2**(numBits - 1)
    return -(int(inputValue) & mask) + (int(inputValue) & ~mask)



device = torch.device('cpu')#'cuda' if torch.cuda.is_available() else torch.device('cpu')

def neuralNetHandler(output_queue,input_queue): #in-out fra lokalt perspektiv
    class modelHandler:
        def __init__(self):

            self.starttid=self.stoptid= time.perf_counter()
            self.model = NeuralNetCtrl()#.to(device)
            checkpoint = torch.load('./chkp2/ctrl/chkpt1.pth')
            self.model.load_state_dict(checkpoint['model_state'])
            #self.model.load()
            self.model.eval()
            self.Output_old=0
            self.state_old=[0.0]*2
            self.durationList=[]
            self.durationListCounter=0

        def shiftRight(self,lst):
            return [0] + lst[:-1]

        def shiftLeft(self,lst):
            return lst[1:] + [0]


        def Do_iteration(self, Data):
            # random moves: tradeoff exploration / exploitation
            # self.starttid=time.perf_counter()

            state0 = torch.tensor(Data, dtype=torch.float)#.to(device='cuda')
            prediction = self.model(state0)

            output = prediction.tolist()
            #output=[0.5,output[0]]
            #print("output: ",len(output))
            return output
    
    modelHandler1=modelHandler()
    
    while(True):
        if(input_queue.empty()):
            pass
        else:
            # sys.stdout.write("out-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
            # sys.stdout.flush() 
            
            DataOut=input_queue.get()
            cmd=DataOut[0]
            if(cmd==1):
                print("inf cmd stop2")
                sys.stdout.flush() 
                break
            elif(cmd==2):
             
                output_queue.put([99])
            else:
                #print(DataOut[1:6],"------------------------------------------------------------------------------------------")

                output=modelHandler1.Do_iteration(DataOut[1:6])
                output_queue.put(output)
                
                


#egen prosess over her


class AgentComm:
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
        self.Id=0
        self.countyCount=0
        self.hzVal=0
        
        self.Extprocess()        


    def Extprocess(self):
        self.p1 = Process(target=neuralNetHandler, args=(self.qIn, self.qOut))
        self.p1.start()


    def normalizeDataIn(self,list):
        tmpf=list[0]*math.pi/180.0
        tmpf2=list[1]*math.pi/180.0
        ans1 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf))
        ans2 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf))
        ans3 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf2))
        ans4 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf2))

        ans5=linearInterpolation(-1.0, 1.0, 0.0, 1.0,list[2] )#pos
        ans6=linearInterpolation(-400.0, 400.0, 0.0, 1.0,list[3] )#dt v1
        ans7=linearInterpolation(-400.0, 400.0, 0.0, 1.0,list[4] )#dt v2
        ans8=linearInterpolation(-1.2, 1.2, 0.0, 1.0,list[5] )#pos dt



        return [0,ans1,ans2,ans3,ans4,ans5,ans6,ans7,ans8] #sin v1, cos v1, sin v2, cos v2, pos, dt v1, dt v2, pos dt, cmd1, cmd2, time cmd
        #0 først er dummy-cmd


    def InferenceIn(self,Id,DataOut):
        if(len(DataOut)>2):
            dataNorm=self.normalizeDataIn(DataOut)
            print("dataNorm: ",dataNorm)
            
        else:
            if(DataOut[0]==1):
                print("inf cmd stop1")
            dataNorm=DataOut
        self.qOut.put(dataNorm)
        
        self.Id=Id
        return



    def normalizeInverse(self,list):#cmdcmdcmdtid
        ans1=int(linearInterpolation(0.0, 1.0, -100.0, 100.0,list[0]) )#cmd1
        ans2=int(linearInterpolation(0.0, 1.0, -100.0, 100.0,list[1] ))#cmd2


        return [ans1,ans2] #cmd1, cmd2, cmd tid


    def InferenceOut(self):
        if(not self.qIn.empty()):
            res=(self.qIn.get())
            idOut=self.Id
            Done=True
            
            if(len(res)>1):
                res=self.normalizeInverse(res)


        else:
            res=[]
            idOut=0
            Done=False

        return res,idOut,Done


