from statistics import stdev
import z_CommonFunc as zcf
import torch

import z_model
from torch.multiprocessing import Process, Queue
import sys
import time





device = torch.device('cpu')#   ('cuda' if torch.cuda.is_available() else torch.device('cpu'))

def PhysSimulator(output_queue,input_queue): #in-out fra lokalt perspektiv
    class modelHandler:
        def __init__(self):


            self.model1 = z_model.NeuralNetIndre ()#.to(device)
            self.model2 = z_model.NeuralNetCart()#.to(device)
            self.model3 = z_model.NeuralNetYtre()#.to(device)
            checkpoint1 = torch.load('./chkp2/phys1/chkpt1.pth')
            checkpoint2 = torch.load('./chkp2/phys2/chkpt1.pth')
            checkpoint3 = torch.load('./chkp2/phys3/chkpt1.pth')
            self.model1.load_state_dict(checkpoint1['model_state'])
            self.model2.load_state_dict(checkpoint2['model_state'])
            self.model3.load_state_dict(checkpoint3['model_state'])

            #self.model.load()
            self.model1.eval()
            self.model2.eval()
            self.model3.eval()

            self.Output_old=0
            self.state_old=[0.0]*2
            self.durationList=[]
            self.durationListCounter=0

            self.PositionData=[0.0,0.5,0.0,0.5,0.5] #pole right down (sin/cos), cart in middle
            self.SpeedData=[0.5,0.5,0.5]
            self.SpeedData2=[0.5,0.5,0.5]            


        def Do_iteration(self, Data):
  
            
            Data[0]=zcf.linearInterpolate(-100,100,0,1,Data[0])
            Data[1]=zcf.linearInterpolate(-100,100,0,1,Data[1])
            #print(self.PositionData ,"        ", Data)
            #print(Data,"data")
                


            vector=self.PositionData +self.SpeedData+ Data
            if(Data[0] > 0.51 or Data[0] < 0.49 or Data[1] > 0.51 or Data[1] < 0.49):
                self.durationListCounter=30
            if(self.durationListCounter > 0):
                self.durationListCounter-=1
                #print(vector,"veccy")



            #.to(device)
    #['v1 sin']	['v1 cos']	[' v2 sin']	['v2 cos']	['pos']	[' dt-v1 ]	[' dt-v2']	[' dt-pos ]	[' act1][' act2']	
    # new dt v2, new dt pos
    
            vector1In=[vector[2],vector[3],vector[6],vector[8]]     #V2 pos
            vector2In=[vector[4],vector[7],vector[9]]               #cart pos

            state1 = torch.tensor(vector1In, dtype=torch.float)
            state2 = torch.tensor(vector2In, dtype=torch.float)

            prediction1 = self.model1(state1)
            prediction2 = self.model2(state2)

            prediction1=prediction1.tolist()
            prediction2=prediction2.tolist()
            vector.append(prediction1[0])
            vector.append(prediction2[0])

#            beforeTime=time.perf_counter()

            state3 = torch.tensor(vector, dtype=torch.float)


            prediction = self.model3(state3)       #XXXXXXXXXXX  forward pass 3 XXXXXXXXXXXXX
            afterTime=time.perf_counter()
            #print("predicition time: ",afterTime-beforeTime)

            deltaValues = prediction.tolist()
            deltaValues.append(prediction1[0])
            deltaValues.append(prediction2[0])
            print(deltaValues,"delta")

            # print(deltaValues,"delta før")
            if(deltaValues[1] < 0.53 and deltaValues[1] > 0.48):
                deltaValues[1]=0.5
            if(deltaValues[2] < 0.51 and deltaValues[2] > 0.49):
                deltaValues[2]=0.5                
            #     print("true true")
            # print(deltaValues,"delta etter")

            self.SpeedData=deltaValues


            #norm v1 v2 pos + delta v1 v2 pos inn, norm v1 v2 pos ut
            self.PositionData=zcf.FindNewPosValues(deltaValues,self.PositionData)


            return self.PositionData
    
    physMod=modelHandler()
    
    dataIn=[-1,0,0]
    oldTime=time.perf_counter()
    newTime = time.perf_counter()
    while(True):
        
        if(not ((newTime-oldTime) >= 0.02)):
            if(not (input_queue.empty())):
                dataIn=input_queue.get()
           
            newTime=time.perf_counter()
            pass
        else:
            # print("ping 2")

            oldTime=time.perf_counter()

            #sys.stdout.flush() 
            # if(dataIn[1]>0.5):
            #     print(dataIn,"inf cmd stop2----_--_--_--_--_--_--_--_--_--_--_--_før  --_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_-")


            cmd=dataIn[0]

            if(cmd==1):
                print("inf cmd stop2")
                sys.stdout.flush() 
                break
            elif(cmd==2):
             
                output_queue.put([99])
            else:
                # print("ping 4")
                # if(dataIn[1]>0.01 or dataIn[1]<-0.01):
                #     print("0 inn i modellen")
                output=physMod.Do_iteration( dataIn[1:3])
                # print("ping 5")
                output_queue.put(output)
                # print("ping 6")
            dataIn=[-1,0,0]


#egen prosess over her----------------------------------------------------------------------------------------------------------------
time.sleep(1)
#

class SimHandler:
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
        self.p1 = Process(target=PhysSimulator, args=(self.qIn, self.qOut))
        self.p1.start()

    def runningf(self,newItem, DataIn, endProg):

        if(newItem):
            DataIn[1]=zcf.twosComplement(DataIn[1],16)
            DataIn[2]=zcf.twosComplement(DataIn[2],16)
            self.qOut.put(DataIn)
        if(not self.qIn.empty()):
            DataOut=self.qIn.get()
    #        ppcs.DoIteration(DataOut)
            self.Id+=1
            dataIn2=zcf.NormToEngPosValues(DataOut)
            return True, [0]+dataIn2+[0,0,0]+[self.Id]
        else:
            return False, False
