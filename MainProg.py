
import time
from tkinter import *
import random
import agent
import guit
import ArduinoCom
import cppComm
import random

import numpy as np

secFlag=False
secFlag20ms=False

secCounter=0
outputSwing=0
outputTravel=0
quitty=False

simulate=True
if __name__ == '__main__':
    

    if(simulate):
        import pygam
        import PhysSim
        simcity=PhysSim.SimHandler()
        time.sleep(1)
        ppcs=pygam.PygameProcess()
        time.sleep(1)
        ppcs.Start()
    else:
        cp=cppComm.commCpp()


    app1 = guit.Appy()
    myAgent=agent.AgentComm()
    myArdCom=ArduinoCom.ArdComm()

def floorCeil(input, floorLim=-100, CeilingLim=100):
    return(min(max(input,floorLim),CeilingLim))

import struct
import numpy as np

def IntTypefloat16_to_float32(x): # Assume that `x` is a variable containing a float16 value stored as an int
    if(simulate):
        return x
    # Extract the exponent and mantissa from `x`
    signBit = (x & 0x8000) << 16 #
    exponent = (x & 0x7C00) >> 10 #7c00 exp<masker 5 bits
    mantissa = (x & 0x03FF) << 13 #10 bits lsb, maske mantissa, legger på 13 nuller 

    exponent += 112 # 112 = 127 - 15, 127 er bias for 32 bit float, 15 er bias for 16 bit float

    # reconstruct the float32 value from the extracted bits
    myFloat = np.float32(0) # 
    myFloat = struct.unpack('!f', struct.pack('!I', signBit | (exponent << 23) | mantissa ))[0]

    return myFloat

def set_bit(value, bit):
    return value | (1<<bit)

def get_bit(value, bit):
    return (value & (1<<bit)) != 0




class mainprog: 
    def __init__(self):

        self.state= []
        self.mode=0
        self.ArdCommOk=False
        self.LogOff=False
        self.LogOn=False
        self.stopping=False
        self.CppOpen=False
        self.counter=0

        self.ManTimeval=0
        self.ManCmdM1=0
        self.ManCmdM2=0

        self.AutCmdM1=0
        self.AutCmdM2=0
        self.CppSts=0
        self.CppCmd=0
        self.M1ActCommand=0
        self.M2ActCommand=0

        self.EndProgram=False
        self.RandPercent=0
        self.CppDataIn=[]
        self.PerfCounter=0
        self.oldTime=self.newTime = time.perf_counter()

        self.test=0

        self.performance=0
        self.ArdDataLast=[0,0,0,0,False ]

        self.NewItemOutgoing=False
        self.newItemIncoming=False
        self.CpConnected=False
        self.InferenceInProg=False
        self.anglErr=False
        self.AnlgeErrCount=0
        self.randTravelSP=0
        self.randTravelStep=0
        self.randTravelActcmd=0

        self.randSwingSP=0
        self.randSwingStep=0
        self.randSwingActcmd=0

        self.keepGoingCount=0




        self.infContactTestinProgress=False
        self.infContact=False
        self.infContactCounter=0

        self.testCounter2=0


        self.IDout=0
        






    def ExchangeDataCP(self):#baseflow in lpm
        
        cmd=0
        dataOut=[0,0,0,0,0,0,0]
        if(self.stopping):
            cmd=2

        if( (self.CppCmd==1)):
            cmd=3

        if(self.LogOn):
            cmd=4

        if(self.LogOff):
            cmd=5

        if(self.EndProgram):
            cmd=2

        if(quitty):
            cmd=1        
            


        dataOut[0]=cmd
        dataOut[1]=self.M1ActCommand
        dataOut[2]=self.M2ActCommand

        dataOut[5]=self.IDout

#//0 sts, 1 v1, 2 v2,3 avst, 4 dv1, 5 dv2, 6 dvAvst, 7 id
        if(simulate):

            self.newItemIncoming,DataIn=simcity.runningf(self.NewItemOutgoing,dataOut,self.EndProgram)
            if(self.newItemIncoming):
                ppcs.DoIteration(DataIn)
        else:
            self.newItemIncoming,DataIn=cp.runningf(self.NewItemOutgoing,dataOut,self.EndProgram)


        if(secFlag):
            self.performance=self.PerfCounter
            self.PerfCounter=0
            self.CpConnected=(self.performance>10)
            if(self.anglErr):
                self.AnlgeErrCount+=1
                if(self.AnlgeErrCount>3):
                    self.anglErr=False
                    self.AnlgeErrCount=0


        if(self.newItemIncoming):
            self.PerfCounter+=1
            self.CppOpen=True
            self.CppSts=DataIn[0]
            # print("cppsts",self.CppSts)
            if(get_bit(self.CppSts,12)):
                self.anglErr=True

            if(self.anglErr):
                self.CppSts=set_bit(self.CppSts,12)

            self.CppDataIn=DataIn[:]
            
            self.v1=IntTypefloat16_to_float32(DataIn[1])
            self.v2=IntTypefloat16_to_float32(DataIn[2])
            self.AVst=IntTypefloat16_to_float32(DataIn[3])
            self.DeltaV1=IntTypefloat16_to_float32(DataIn[4])
            self.DeltaV2=IntTypefloat16_to_float32(DataIn[5])
            self.DeltaVAvst=IntTypefloat16_to_float32(DataIn[6])
            self.IncomID=DataIn[7]
        
    def ExchangeDataArd(self,tick):#
        
        DataOut=[0,0,0,0,0 ,False]

        tmpAct1=0
        tmpAct2=0




        if(self.mode==1):
            tmpAct1=self.ManCmdM1
            tmpAct2=self.ManCmdM2

        if(self.mode==2):#rand mixed with inference
            tmpAct1=self.AutCmdM1
            tmpAct2=self.AutCmdM2




        if(quitty):
            DataOut[0]=1

        self.ArdCommOk=True




        if(tmpAct1<0):
            DataOut[1]=int(tmpAct1 ) & 0xFFFF
        else:
           DataOut[1]=int(tmpAct1 ) 


        if(tmpAct2<0):
            DataOut[2]=int(tmpAct2 ) & 0xFFFF
        else:
            DataOut[2]=int(tmpAct2 )

        
        if(self.ArdCommOk):
            self.M1ActCommand=DataOut[1]
            self.M2ActCommand=DataOut[2]
      


        # DataOut[1]=0
        # DataOut[2]=

        
        DataOut[0]=int(self.EndProgram)


        DataOut[5]=(self.NewItemOutgoing)
        
        # if(newItem):
        #     print("newItem")
        myArdCom.running(DataOut)
        self.ArdDataLast=DataOut[:]


        

    def StateMachine(self, stateIn):
        global secCounter
        global secFlag

        if (stateIn==0):
            if(self.ArdCommOk):
                return(1)
            else:
                return(0)

        if (stateIn==1):
            if(self.CppOpen): #popen
                return (4)
            else:
                return(1)

        if (stateIn==4):
            if(secFlag):
                secCounter+=1


            if(secCounter>2):
                secCounter=0
                return (5)
            else:
                return (4)

        if (stateIn==5):
            #cp.interpretCommand(2) ##start datautveksling
            return (6)

        if (stateIn==6):
            if(self.CppSts==4):
                return (7)
            else:
                return (6)


        if (stateIn==7):
                return (7)



    def updateGuiData(self):

        self.RandPercent=app1.ValDict["Random"].get()
        # app1.n.set(dpd+1)
        self.mode=app1.mode
        self.EndProgram=app1.endButton
        if(not app1.is_alive()):
            return(0)

        if app1.LogOn:
            app1.LogOn=False

            self.LogOn=True
            self.LogOff=False

           # app1.ValDict["outCmdCpp"].set((self.CppCmd))
        if app1.LogOff:
            app1.LogOff=False
            self.LogOff=True
            self.LogOn=False


        if app1.startCppComm:
            app1.startCppComm=False

        if app1.stopCppComm:
            app1.stopCppComm=False

        if app1.specialCppComm:
            tmmp=self.CppCmd

            if(tmmp==1):
                self.CppCmd=0
            if(tmmp==0):
                self.CppCmd=1


            app1.ValDict["outCmdCpp"].set((self.CppCmd))

            app1.specialCppComm=False

        if (secFlag):
            print("secFlag")

        if(secFlag and (len(self.CppDataIn)>3)):
            #print("self.v1,self.v2,self.AVst,self.DeltaV1,self.DeltaV2,self.DeltaVAvst",[self.v1,self.v2,self.AVst,self.DeltaV1,self.DeltaV2,self.DeltaVAvst])

            app1.ValDict["angle1"].set('{number:.{digits}f}'.format(number=self.v1, digits=2))# comment
            app1.ValDict["angle2"].set('{number:.{digits}f}'.format(number=self.v2, digits=2))# comment
            app1.ValDict["angle1Dt"].set('{number:.{digits}f}'.format(number=self.DeltaV1, digits=2))# comment
            app1.ValDict["angle2Dt"].set('{number:.{digits}f}'.format(number=self.DeltaV2, digits=2))# comment
            app1.ValDict["CppState"].set((0xFF & self.CppSts))# comment
            app1.ValDict["Py_State"].set((currState))# comment
            app1.ValDict["HzIn"].set(self.performance)# comment
            app1.ValDict["VognPos"].set( '{number:.{digits}f}'.format(number=self.AVst, digits=2))# comment
            app1.ValDict["pos DV"].set( '{number:.{digits}f}'.format(number=self.DeltaVAvst, digits=2))# comment



            app1.SetRadiobuttons(0,0xFF00 & self.CppDataIn[0])#0xFF00 & fordi 2 ls bytes er for tidligere kommando
            if (self.infContact):
                tesss=1
            else:
                tesss=0
            app1.SetRadiobuttons(1,(tesss))#self.ArdCommOk & 

    def WaitState(self):
        self.NewItemOutgoing=secFlag

    def manualControl(self,tick):
        self.NewItemOutgoing=False
        if not tick:
            return  


        if (app1.M1left or app1.M1right or app1.M2left or app1.M2right):
            self.ManCmdM1=0
            self.ManCmdM2=0            
            pwrval=app1.ValDict["pwr"].get()
            self.keepGoingCount=int(app1.ValDict["time"].get()/10)


            if (app1.M1left):
                self.ManCmdM1=pwrval

            if (app1.M2left):
                self.ManCmdM2=pwrval

            if (app1.M1right):
                self.ManCmdM1=(pwrval*(-1)) #& 0xFFFF

            if (app1.M2right): 
                self.ManCmdM2=(pwrval*(-1)) #& 0xFFFF
            
            
            app1.M1left =False
            app1.M1right =False
            app1.M2left =False
            app1.M2right=False
        else:
            if(self.keepGoingCount>0):
                self.keepGoingCount-=1
            else:
                self.ManCmdM1=0
                self.ManCmdM2=0
        self.NewItemOutgoing=True

    def Ramp(self, valueSp, ValueIs, rampStep):
        if (valueSp>ValueIs):
            ValueIs+=rampStep
            if (valueSp<ValueIs):
                ValueIs=valueSp
        else:
            ValueIs-=rampStep
            if (valueSp>ValueIs):
                ValueIs=valueSp
        return ValueIs

    def ShutDownInference(self):
            myAgent.InferenceIn(99,[1])


    def TestInferenceContact(self,tick):

        if(not (self.infContactTestinProgress)):
            myAgent.InferenceIn(99,[2])
            self.infContactTestinProgress=True
            self.infContactCounter=0

        else:
            res=myAgent.InferenceOut()
            if(res[2] and (res[0][0]==99)): # res,idOut,Done
                self.infContact=True
                self.infContactCounter=0
                self.infContactTestinProgress=False
                
            else:
                self.infContactCounter+=1
                if(self.infContactCounter>50):
                    self.infContact=False
                    self.infContactCounter=0
                    self.infContactTestinProgress=False
        return

    def RandomControl(self, ideas, incoming):
        
        # if not tick:
        #     return  
        if(secFlag):
            self.testCounter2+=1
        
        if(self.testCounter2>40):
            self.testCounter2=0

        if(self.testCounter2<4):
            takeitslow=False
        else:
            takeitslow=True

        global outputSwing
        global outputTravel

        if(self.InferenceInProg):

            
            
            result,self.IDout,IsDone=myAgent.InferenceOut() #agent->main
            if(IsDone and len(result)>1):

                self.InferenceInProg=False
                self.AutCmdM1=result[0]
                self.AutCmdM2=result[1]

                # outputTravel=result[1]
                self.NewItemOutgoing=True
                return
            else:

                return

        if(not incoming):



            return

        
        if((self.RandPercent==0) or (self.RandPercent<random.randint(0, 100))):


            myAgent.InferenceIn(self.IncomID,[self.v1,self.v2,self.AVst,self.DeltaV1,self.DeltaV2,self.DeltaVAvst]) #main -> agent
            self.InferenceInProg=True
            return


        #kun random
        randomTravel=False
        randomSwing=False


        randType=random.randint(0, 29)

        if(randType<2):
            randomTravel=True

        if(randType>2 and randType<5):
            randomSwing=True



        InDangerZoneGoRight=((self.AVst)<-0.83)
        InDangerZoneGoLeft=((self.AVst)>0.83)
            

        if(randomTravel or InDangerZoneGoLeft or InDangerZoneGoRight):
            if(self.AVst<0):
                minSp=-68
                maxSp=100
            else:
                minSp=-100
                maxSp=68

            if(InDangerZoneGoLeft):
                print("InDangerZoneGoLeft")
                minSp=-100
                maxSp=0
            if(InDangerZoneGoRight):
                print("InDangerZoneGoRight:" + str(self.randTravelActcmd))
                minSp=0
                maxSp=100
            self.randTravelSP=(random.randint(minSp, maxSp))
            print(f"{self.randTravelSP} : rand")

            self.randTravelStep=(random.randint(2, 10))

        if(randomSwing):
            self.randSwingSP=(random.randint(-60, 60))
            self.randSwingStep=(random.randint(2, 10))



#neg er mot venstre, pos mot høyre
        if(takeitslow):
            
            self.randSwingActcmd=0
        else:
            
            self.randSwingActcmd=self.Ramp(self.randSwingSP, self.randSwingActcmd, self.randSwingStep)
        
        self.randTravelActcmd=self.Ramp(self.randTravelSP, self.randTravelActcmd, 1)




        # if(self.randTravelActcmd<0):
        #     self.AutCmdM2=int(self.randTravelActcmd ) & 0xFFFF
        # else:
        #     self.AutCmdM2=int(self.randTravelActcmd ) 

        self.AutCmdM2=int(self.randTravelActcmd )
        # if(self.randSwingActcmd<0):
        #     self.AutCmdM1=int(self.randSwingActcmd ) & 0xFFFF
        # else:
        #     self.AutCmdM1=int(self.randSwingActcmd )
        self.AutCmdM1=int(self.randSwingActcmd )

        if(self.IDout==ideas):
            print("IDout==IncomID-----------------------------------------------------------")

        self.IDout=ideas
        self.NewItemOutgoing=True



    def Loadmodel(self):
        pass


bigP=mainprog()

#def main():





if __name__ == '__main__':

    oldTime=newTime = time.perf_counter()
    oldTime20ms=newTime20ms = time.perf_counter()
    currState=0
    CppState=0
    
    counterr=0


    testCounter=0
    lastId=0
    while(True):

        
        newTime = time.perf_counter()
        deltaTime=newTime-oldTime
        secFlag=False
        if(deltaTime>1):
            oldTime=newTime = time.perf_counter()
            secFlag=True

            # print(f"testCounter MAIN {testCounter} hz")
            testCounter=0
            
        newTime20ms = time.perf_counter()
        deltaTime20ms=newTime20ms-oldTime20ms
        secFlag20ms=False
        if(deltaTime20ms>0.02):
            oldTime20ms = time.perf_counter()
            secFlag20ms=True



        ticker=False
        if(bigP.CpConnected):
            ticker=bigP.newItemIncoming
        else:
            ticker=secFlag20ms

        if(ticker):
            testCounter+=1

        if(bigP.newItemIncoming):
            if(bigP.IncomID==lastId):
                print("duplicate id ------------------------------------")
            lastId=bigP.IncomID

        

        bigP.updateGuiData()
        bigP.ExchangeDataCP()
        bigP.NewItemOutgoing=False


        if(bigP.mode == 0):
            bigP.WaitState()

        if(bigP.mode == 1):
            bigP.manualControl(ticker)

        if(bigP.mode == 2):
            bigP.RandomControl(bigP.IncomID,bigP.newItemIncoming)
        else:
            bigP.TestInferenceContact(ticker)

        currState=bigP.StateMachine(currState)



        bigP.ExchangeDataArd(ticker)
        




        

        


        
        if (bigP.EndProgram):
            bigP.ShutDownInference()
            myArdCom.shutDown()


            break


    print("q123")
    app1.root.quit()
    time.sleep(0.1)
    print("q1234")
