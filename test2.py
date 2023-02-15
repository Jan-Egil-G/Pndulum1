import math
import random

def linearInterpolation(x1, x2,  y1,y2, x):
    return y1 + (x - x1) * ((y2 - y1) / (x2 - x1))
def xx(v1,v2):
    tmpf=v1*math.pi/180.0
    tmpf2=v2*math.pi/180.0
    ans1 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf))
    ans2 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf))
    ans3 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf2))
    ans4 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf2))
    return [ans1,ans2,ans3,ans4]

def yy():
    ans1=random.uniform(0.0, 1.0)
    ans2=random.uniform(0.0, 1.0)
    ans3=random.uniform(0.0, 1.0)
    return [ans1,ans2,ans3]


def WriteToFile(Plist):
    with open(f"C:/PyPj/doublepend2/LogDir/Log_0.csv", 'w') as f:
        f.write("v1s, v1cos,v2s, v2cos,pos, v1dt,v2dt,posdt,cmd1,cmd2\n")
        
#                for sublist in Plist:
        for sample in Plist:#sublist:
            for i,item in enumerate(sample):
                if(i>0):
                    f.write(",")

                f.write("%s " % item)
            f.write("\n")
        
    print("file written")

final=[]
for k in range(0,10):
    for i in range(0,100):
        for j in range(0,100):
            V1=random.uniform(0.0, 360.0)
            V2=float(i*3.60)
            pos=[j*0.01]

            out1=0.5

            if(V2>115.0 and V2<265.0):
                out1=0.2

            if(V2<65.0 or V2>275.0):
                out1=0.8

            if(pos[0]>0.55):
                out2=0.25

            if(pos[0]<0.45):
                out2=0.75


            list=xx(V1,V2)
            list2=yy()
            final.append(list +pos + list2 + [out1,out2])

WriteToFile(final)

