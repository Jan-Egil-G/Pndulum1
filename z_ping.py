

#læring steg 2
#pingpong
from queue import Queue

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

def ping(minQval,LengthOfLine,numlogs,startline,stopline):
    qlistTotal=[]
    log_i=0

    n1=8#stride
    class MyDataset(Dataset):
        def __init__(self):#
            xy= np.loadtxt(f"./LogDir/norm/Log_{log_i}.csv", delimiter=',', dtype=np.float32, skiprows=startline,max_rows=stopline-startline)


            self.n_samples = xy.shape[0]
            self.xdata  = torch.from_numpy(xy[:, [0,1,2,3,4,5,6,7,8,9]]) ##sin v1, cos v1, sin v2, cos v2, pos, dt v1, dt v2, pos dt, cmd1, cmd2, time cmd, tcmd2 

        def __getitem__(self, index):
            return self.xdata[index]

        def __len__(self):
            return (self.n_samples)


    dataset = MyDataset()
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False) #alle verdier er normalisert








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

        
    def WriteToFile(Plist):
        with open(f"C:/PyPj/doublepend2/LogDir/pingpong/Log_{log_i}.csv", 'w') as f:
            f.write("v1s, v1cos,v2s, v2cos,pos, v1dt,v2dt,posdt,cmd1,cmd2,cmdtime1,cmdtime2 \n")
            
#                for sublist in Plist:
            for sample in Plist:#sublist:
                for i,item in enumerate(sample):
                    if(i>0):
                        f.write(",")

                    f.write("%s " % item)
                f.write("\n")

        print("file written")


    startpointsprocessed=0
    finalList=[]
    Qlist=[]
    q = Queue()
    lastQv=0
    print("starting loop ping")
    for i,sample in enumerate(dataloader):

        if((i % 1000) ==0):
            print(f"i: {i}")

        sampleList=sample.tolist()[0]
        #sampleList er en sample fra logg. 

        rr=5
        Qv=zcf.Qvalue(sampleList)

        startvector=[]


        if(Qv>minQval and i>(1+LengthOfLine)):

            Plist=list(q.queue)

            Qv2=zcf.Qvalue(Plist[0])
            if(Qv>(Qv2+minQval) and ((lastQv+0.01) > Qv)):#må være bedre enn første element i køen

                for x,item in enumerate(Plist):
                    finalList.append(item[:])
                startpointsprocessed+=1

                Qlist.append(Qv)
        lastQv=Qv

        q.put(sampleList)

        if(i>=(LengthOfLine)):
            q.get()




    print(f"ant rekker funnet (X lengde linje): {startpointsprocessed}")

    WriteToFile(finalList)

    qlistTotal.append(Qlist[:])
        #print(f"qlistTotal: {(qlistTotal)}")
    return qlistTotal
    















