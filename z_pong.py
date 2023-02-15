

#læring steg 2
#pingpong
import z_model
import y_model

import torch
import z_CommonFunc as zcf
import torch.nn as nn
import numpy as np
import random
from torch.utils.data import Dataset, DataLoader
import math
# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

oneshot=False


    # 	N5=10# N5 is the lenght of prediction line
    # 	N2=3 # N2 is number of prediction lines pr starting point

def limit(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x

def pong(minq,NumLines,NumBetwRand,LengthOfLine,startline,stopline):
    qlistTotal=[]
    # for log_i in range(numlogs):
    # print(f"working on log {log_i}")

    n1=9#stride
    class MyDataset(Dataset):
        def __init__(self):#
            xy= np.loadtxt(f"./LogDir/norm/Log_0.csv", delimiter=',', dtype=np.float32, skiprows=startline,max_rows=stopline-startline)


            self.n_samples = xy.shape[0]
            self.xdata  = torch.from_numpy(xy[:, [0,1,2,3,4,5,6,7,8,9]]) ##sin v1, cos v1, sin v2, cos v2, pos, dt v1, dt v2, pos dt, cmd1, cmd2,

        def __getitem__(self, index):
            return self.xdata[index]

        def __len__(self):
            return (self.n_samples)


    dataset = MyDataset()
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False) #alle verdier er normalisert


    if(NumBetwRand!=1):
        modelCtrl = y_model.NeuralNetCtrl().to(device)
        
        modelCtrl.eval()


    # checkpoint = torch.load('./chkp2/ctrl/chkpt1.pth')
    # modelCtrl.load_state_dict(checkpoint['model_state'])

    #epoch = checkpoint['epoch']

    modelPhys = z_model.NeuralNet().to(device)
    checkpoint = torch.load('./chkp2/phys/chkpt1.pth')
    modelPhys.load_state_dict(checkpoint['model_state'])
    modelPhys.eval()
    #epoch = checkpoint['epoch']

    counter=0




    def linearInterpolate(x1, x2, y1, y2, x):
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)





    def regnTilbakeVinkler(sinVal,cosval):
        sinx=linearInterpolate(0.0, 1.0, -1.0, 1.0, sinVal)
        cosx=linearInterpolate(0.0, 1.0, -1.0, 1.0, cosval)
        vinkl=math.atan2(sinx,cosx)*180.0/math.pi
        if (vinkl<0):
            vinkl=vinkl+360.0
        return vinkl

    def regnTilleggVinkler(dtV1,dtV2):
        dtV1Deg=linearInterpolate(0.0, 1.0, -400.0, 400.0, dtV1)
        dtV2Deg=linearInterpolate(0.0, 1.0, -400.0, 400.0, dtV2)
        return dtV1Deg, dtV2Deg


    def linearInterpolation(x1, x2,  y1,y2, x):
        return y1 + (x - x1) * ((y2 - y1) / (x2 - x1))




    def normalizeFloatList(list):
        tmpf=list[0]*math.pi/180.0
        tmpf2=list[1]*math.pi/180.0
        ans1 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf))
        ans2 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf))
        ans3 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf2))
        ans4 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf2))

        ans5=linearInterpolation(-1.0, 1.0, 0.0, 1.0,list[2] )#pos

        return [ans1,ans2,ans3,ans4,ans5]

    def MakePredictionLine(startvec, modelCtrl, modelPhys):
        global oneshot
        predLineList=[]

        workingState=startvec[:]  #
        

        ###startvector; v1s, v1cos,v2s, v2cos,pos, dt,dt,dt,cmd,cmd,, 0-9

        for j in range(NumLines): # N2 is number of prediction lines pr starting point
            predLineList.append([])
#                predLineList[j].append(startvec[:])
            
            
            for i in range(LengthOfLine): # N5 is the lenght of prediction line


                #T0
                #-_-_-_-_-_-_-_-_-_-_-_-_-_-_phys module begin-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

                ws2=workingState[:]

                ws2=torch.FloatTensor(ws2).to(device='cuda')            
                
                newAngles=(modelPhys(ws2)) # marks new timestep -------------------------------------forward pass phys
                newAngles=newAngles.tolist() #angles and pos (DT)

        
                vink1=regnTilbakeVinkler(workingState[0],workingState[1])
                vink2=regnTilbakeVinkler(workingState[2],workingState[3])
                dtV1,dtV2=regnTilleggVinkler(newAngles[0],newAngles[1])


                vink1=vink1+dtV1 #ny vinkel, ikke normalisert
                vink2=vink2+dtV2 #ny vinkel, ikke normalisert

                
                newPosDt=linearInterpolate(0.0, 1.0, -1.2, 1.2, newAngles[2])
                OldPos=linearInterpolate(0.0, 1.0, -1.0, 1.0, workingState[4])

                newPos=OldPos+newPosDt #ny pos, ikke normalisert
                newPos=limit(newPos,-1.1,1.1)

                normNew=normalizeFloatList([vink1,vink2,newPos]) #normaliserer vinkler og pos

                workingState[0:5]=normNew[:]  #v1s, v1cos,v2s, v2cos,pos

                workingState[5:8]=newAngles[:] #dt,dt,dt

                #startvector; v1s, v1cos,v2s, v2cos,pos, dt,dt,dt,cmd,cmd,cmd,

                #-_-_-_-_-_-_-_-_-_-_-_-_-_-_phys module end-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

                #T1


                #-_-_-_-_-_-_-_-_-_-_-_-_-_-_ctrl module begin-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

                #WsIn=workingState[:] #working state; all values normalized

                randAddAct1=0.0
                randAddAct2=0.0
                if(NumBetwRand==1):
                    x1=0.0
                    x2=1.0
                else:
                    x1=-0.3
                    x2=0.3

                if((i % NumBetwRand) == 0):
                    randChoice=random.randint(1, 4)
                    
                    if((randChoice == 1) or (randChoice == 4)):
                        randAddAct1=random.uniform(x1, x2)

                    if((randChoice > 2)):
                        randAddAct2=random.uniform(x1, x2)   

                if(NumBetwRand!=1):
                    wss=workingState[:]
                    wss=torch.FloatTensor(wss).to(device='cuda')

                    currAct=(modelCtrl(wss))   #-------------------------------------forward pass ctrl
                    # print(f"currAct {len(currAct)}")
                    currAct=currAct.tolist()



                    # print(f"currAct tid {currAct[2]}")
                    
                    # print(f"workingState {len(workingState)}")

                    workingState[8]=limit(currAct[0]+randAddAct1,0.0,1.0)#currAct[0]+
                    workingState[9]=limit(currAct[1]+randAddAct2,0.0,1.0)
                else:
                    workingState[8]=randAddAct1
                    workingState[9]=randAddAct2


                #-_-_-_-_-_-_-_-_-_-_-_-_-_-_ctrl module end-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

                #T1+dt

                SaveState=workingState[:]


                predLineList[j].append(SaveState[:])

        

        #all lines are now made, find the best one


        HighQval=[0.0,-1,-1]
        HQ2=0.0
        StartQ=0.0

        for j, linelist in enumerate(predLineList):#dette er alle lin jene for et startpunkt
            # if(j==0):
            #     continue
            for i, sample in enumerate(linelist):#dette er alle samples/punkter i en linje
                # if(i==0):
                #     continue

                Qval=zcf.Qvalue(sample)
                if(i==0):
                    StartQ=Qval
                    continue


                if abs(Qval)>HQ2 and abs(Qval)>minq:#må være over minstekriteriet og større enn alle før
                    HighQval=[Qval,i,j]
                    HQ2=abs(Qval)
        
        # if(HighQval[1] != 0):
        #     print("------------------------------gogo-------------------------------------")

        if(HighQval[1] == -1):            
            return -1, []
        else:
            returnlist=predLineList[HighQval[2]][:HighQval[1]] #[beste linje][slutter 1 før topp]

        # print(f"HighQval {HighQval}")
        return HighQval[0],returnlist


        
    def WriteToFile(Plist):
        with open(f"C:/PyPj/doublepend2/LogDir/pingpong/Log_0.csv", 'w') as f:
            f.write("v1s, v1cos,v2s, v2cos,pos, v1dt,v2dt,posdt,cmd1,cmd2,cmdtime, GT cmd1,GT cmd2,GT cmd tid\n")
            
#                for sublist in Plist:
            for sample in Plist:#sublist:
                for i,item in enumerate(sample):
                    if(i>0):
                        f.write(",")

                    f.write("%s " % item)
                f.write("\n")
                # f.write("\n")
                # f.write("\n")
            
        print("file written")


    startpointsprocessed=0
    finalList=[]
    Qlist=[]
    print("starting loop pong")
    for i,sample in enumerate(dataloader):
        sampleList=sample.tolist()[0]

        if i==0:
            lastSample=sampleList
        counter+=1
        if(counter < n1):
            lastSample=sampleList #sample; v1, v2, pos, act1, act2
            continue
        counter=0

        print(f"startpoint no: {i}")

    #sampleList er en sample fra logg. 
        


        startvector=sampleList[0:12]#startvector; v1s, v1cos,v2s, v2cos,pos, dt,dt,dt,cmd,cmd,cmd,

        startpointsprocessed+=1
        if(NumBetwRand==1):
            modelCtrl="none"

        Qv, Plist=MakePredictionLine(startvector, modelCtrl, modelPhys)
        print(Plist)
        #print(f"Qv: {len(Plist)}")
        for item in Plist:
            # if(len(item)>12):
            #     print("workingState too long")
            finalList.append(item[:])
        Qlist.append(Qv)



    print(f"startpointsprocessed: {startpointsprocessed}")

    WriteToFile(finalList)

    qlistTotal.append(Qlist[:])
    print(f"qlistTotal: {(qlistTotal)}")
    return qlistTotal
    















