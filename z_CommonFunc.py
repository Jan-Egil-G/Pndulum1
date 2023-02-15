import matplotlib.pyplot as plt
import numpy as np

import math

curveV=[[0,2],[7,0.7],[20,0.2],[40,0.1],[180.1,0.01]]


curvePos=[[0,2],[0.6,0.8],[0.8,0.1],[1.1,0.01]]
curveVdt=[[0,2],[0.2,0.7],[0.6,0.1],[1.1,0.01]]
curvePosdt=[[0,2],[0.2,0.7],[0.65,0.17],[1.1,0.01]]

#norm/eng converter non linear
curveV1dt=[[0,0],[0.002,0.5],[0.4,35.0],[0.5,170.0]]
curveV2dt=[[0,0],[0.002,0.5],[0.4,20.0],[0.5,150.0]]
curvePosdt=[[0,0],[0.002,0.01],[0.4,0.3],[0.5,0.8]]


def linearInterpolate(x1, x2, y1, y2, x):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

def CurveGetter2(x, curve, Yinput):

    x=abs(x)

    xx=0
    for datap in curve:
        if(x<datap[int(Yinput)]):
            break
        xx=xx+1

#2
    if((xx+1)>len(curve)):
        xx=xx-1 #extrapolering heller enn interpolering


    if (Yinput):
        rr=linearInterpolate(curve[xx-1][1], curve[xx][1], curve[xx-1][0], curve[xx][0], x)
    else:
        rr=linearInterpolate(curve[xx-1][0], curve[xx][0], curve[xx-1][1], curve[xx][1], x)


    return (rr)

def CurveGetter(x, curve):

    x=abs(x)

    xx=0
    for datap in curve:
        if(x<datap[0]):
            break
        xx=xx+1

#2

    if((xx+1)>len(curve)):
        return 0.001

    rr=linearInterpolate(curve[xx-1][0], curve[xx][0], curve[xx-1][1], curve[xx][1], x)


    return (rr)

def SpeedNormalizeAndCap(speed):
    if(speed < 0.0):
        speed= 0.0
    if(speed > 1.0):
        speed= 1.0
    return abs(speed-0.5)*2

def Qvalue(state):
                    #sin v1, cos v1, sin v2, cos v2, pos, dt v1, dt v2, pos dt, cmd1, cmd2, time cmd ,2



    lb1=state
    V1dgr=math.acos(state[0])*57.296 # 0.0-180.0, hvor 0 er rett opp. 90 enten venstre eller høyre
    V2dgr=math.acos(state[2])*57.296 # arccos(sin(x))
    #SpeedNormalizeAndCap; cap'er inn sig til 0-1, og skalerer -1 til 1 og returnener Abs det
    Posnorm=SpeedNormalizeAndCap(state[4]) #bruker speed func, den vireker her og
    # V1dtabs=SpeedNormalizeAndCap(state[5]) # 0.0-1.0 abs speed

    # V2dtabs=SpeedNormalizeAndCap(state[6])
    # Posdtnorm=SpeedNormalizeAndCap(state[7]) #bruker speed func, den vireker her og
  #  l2=[V1dgr, V2dgr, Posnorm, V1dtabs, V2dtabs, Posdtnorm]

    Qv1=CurveGetter(V1dgr, curveV) # 0.0-180.0
    Qv2=CurveGetter(V2dgr, curveV) # 0.0-180.0
    Qpos=CurveGetter(Posnorm, curvePos)  


  #  lb3=[Qv1,Qv2,Qpos,Qv1dt,Qv2dt,QvposDt]
    Q=Qv1*Qpos#*Qv1dt*Qv2dt*QvposDt# Qpos*Qv1#
    lb4=Q


    return Q

def plotQcurves(dtCurves):

    if dtCurves:
        curve1=curveV1dt
        curve2=curveV2dt
        curve3=curvePosdt
    else:
        curve1=curvePos
        curve2=curveVdt
        curve3=curveV
    x = [point[0] for point in curve1]
    y = [point[1] for point in curve1]
    plt.plot(x, y, linestyle='-')

    x = [point[0] for point in curve2]
    y = [point[1] for point in curve2]
    plt.plot(x, y, linestyle='-')

    # x = [point[0] for point in curvePosdt]
    # y = [point[1] for point in curvePosdt]
    # plt.plot(x, y, linestyle='-')

    plt.show()
    
    x = [point[0] for point in curve3]
    y = [point[1] for point in curve3]
    plt.plot(x, y, linestyle='-')

    plt.show()

def plotbar(values):


    # Minimum and maximum values of the list
    min_val = min(values)
    max_val = max(values)

    # Create an array of 7 evenly spaced values between the minimum and maximum values
    bins = np.linspace(min_val, max_val, 8)

    # Use the digitize function to group the values into the corresponding intervals
    digitized = np.digitize(values, bins)




    # Create a bar plot of the group counts
    plt.hist(digitized, bins=range(1,8))
    plt.xlabel('Groups')
    plt.ylabel('Counts')

    # Create a list of the interval ranges for each group
    interval_ranges = ["(%.6f, %.6f]" % (bins[i-1], bins[i]) for i in range(1, len(bins))]

    # Set the x-tick labels for the bar plot
    plt.xticks(range(1,8), interval_ranges, rotation=16)
    plt.show()

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
    dtV1Deg=dtValuesNormToEng(dtV1,True,False,False)
    dtV2Deg=dtValuesNormToEng(dtV2,False,True,False)
    return dtV1Deg, dtV2Deg

def normalizeFloatList(list):
    tmpf=list[0]*math.pi/180.0
    tmpf2=list[1]*math.pi/180.0
    ans1 = linearInterpolate(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf))
    ans2 = linearInterpolate(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf))
    ans3 = linearInterpolate(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf2))
    ans4 = linearInterpolate(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf2))

    ans5=linearInterpolate(-1.0, 1.0, 0.0, 1.0,list[2] )#pos

    return [ans1,ans2,ans3,ans4,ans5]

def limit(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x

def FindNewPosValues(deltaValues,posData):
    vink1=regnTilbakeVinkler(posData[0],posData[1])
    vink2=regnTilbakeVinkler(posData[2],posData[3])

    dtV1,dtV2=regnTilleggVinkler(deltaValues[0],deltaValues[1])

    vink1=vink1+dtV1 #ny vinkel, ikke normalisert
    vink2=vink2+dtV2 #ny vinkel, ikke normalisert


    newPosDt=dtValuesNormToEng(deltaValues[2],False,False,True)/10.0

    OldPosEng=linearInterpolate(0.0, 1.0, -1.0, 1.0, posData[4])


    newPos=OldPosEng+newPosDt #ny pos, eng values



    newPos=limit(newPos,-1.2,1.2)

    posData=normalizeFloatList([vink1,vink2,newPos])

    return posData

def NormToEngPosValues(posData):
    vink1=regnTilbakeVinkler(posData[0],posData[1])
    vink2=regnTilbakeVinkler(posData[2],posData[3])


    OldPos=linearInterpolate(0.0, 1.0, -1.0, 1.0, posData[4])
    newPos=limit(OldPos,-1.2,1.2)


    return [vink1,vink2,newPos]

def dtValuesNormToEng(x,V1,V2,Pos):
    xx=x-0.5
    invert=False
    if xx<0:
        xx=xx*-1
        invert=True

    if(V1):
        curve=curveV1dt
    elif(V2):
        curve=curveV2dt
    elif(Pos):
        curve=curvePosdt
    else:
        print("ERROR: No curve selected")
        return 0

    y=(CurveGetter2(xx, curve,False))#true; eng to norm, false; norm to eng

    if invert:
        y=y*-1
    
    return y

def dtValuesEngToNorm(x,V1,V2,Pos):
    xx=x
    invert=False
    if xx<0:
        xx=xx*-1
        invert=True

    if(V1):
        curve=curveV1dt
    elif(V2):
        curve=curveV2dt
    elif(Pos):
        curve=curvePosdt
    else:
        print("ERROR: No curve selected")
        return 0

    y=(CurveGetter2(xx, curve,True))#true; eng to norm, false; norm to eng

    if invert:
        y=y*-1

    y=y+0.5
    return y

def twosComplement(inputValue, numBits):
    mask = 2**(numBits - 1)
    return -(int(inputValue) & mask) + (int(inputValue) & ~mask)