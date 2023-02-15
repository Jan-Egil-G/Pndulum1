import csv
import math
# Set the starting number and ending number for the files

# Initialize an empty list to store the lines from the files
lines = []
import z_CommonFunc as zcf


def linearInterpolation(x1, x2,  y1,y2, x):
    return y1 + (x - x1) * ((y2 - y1) / (x2 - x1))


def twosComplement(inputValue, numBits):
    mask = 2**(numBits - 1)
    return -(int(inputValue) & mask) + (int(inputValue) & ~mask)




def normalizeFloatList(list):
    tmpf=list[0]*math.pi/180.0
    tmpf2=list[1]*math.pi/180.0
    ans1 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf))
    ans2 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf))
    ans3 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.sin(tmpf2))
    ans4 = linearInterpolation(-1.0, 1.0, 0.0, 1.0,math.cos(tmpf2))

    ans5=linearInterpolation(-1.0, 1.0, 0.0, 1.0,list[2] )#pos
    ans6=zcf.dtValuesEngToNorm(list[3],True,False,False)#dt v1
    ans7=zcf.dtValuesEngToNorm(list[4],False,True,False)#dt v2
    ans8=zcf.dtValuesEngToNorm(list[5],False,False,True)#dt v2

    tmp=twosComplement(list[6],16)
    ans9=linearInterpolation(-100.0, 100.0, 0.0, 1.0,tmp )#
    tmp=twosComplement(list[7],16)
    ans10=linearInterpolation(-100.0, 100.0, 0.0, 1.0,tmp )#



    return [ans1,ans2,ans3,ans4,ans5,ans6,ans7,ans8,ans9,ans10] #sin v1, cos v1, sin v2, cos v2, pos, dt v1, dt v2, pos dt, cmd1, cmd2, time cmd

def PrepData():
    # Loop through the files

    filename = "C:/PyPj/doublepend2/LogDir/prenorm/Log_0.csv"
    with open(filename, "r") as f:
        # Read the file to a list of lines
        file_lines = f.readlines()
        # Add the lines to the list
        lines=(file_lines)


    firstline=[["v1 sin"],["v1 cos"],[" v2 sin"],["v2 cos"],["pos"],[" dt-v1 (dgr pr sec)"],[" dt-v2"],[" dt-pos (pct pr sec)"],[" act1 (raw)"],[" act2"],[" lbl v1 (0-360)"],[" v2 lbl"],["  pos lbl"]]
    # Print the lines
    AllList = []
    float_list2=[]
    float_list3=[]
    float_list4=[]
    print("prpData")
    print("\n")
    for i,line in enumerate(lines):
        print(i)
        if(i==0):
            continue


        float_list = [float(x) for x in line.split(",")[5:13]]
        # print("float_list",float_list)
        # print("\n")
        if(i>1):
            float_list3=float_list2[:12]#normaliserte lister
            # float_list4=float_list2[12:]

        float_list2=normalizeFloatList(float_list[:])
        # print("float_list2",float_list2)
        # print("\n")
        float_list3.extend(float_list2[5:8])  #1 og 2:labels eller "fremtidsverdier" . 3 og 4 current, men forrige iterasjon


        if(i>1):
            AllList.append(float_list3[:])



    filename = "C:/PyPj/doublepend2/LogDir/norm/Log_0.csv"

    with open(filename, "w", newline="") as f:
        # Create a CSV writer

        writer = csv.writer(f)
        writer.writerow(firstline)
        # Write the data to the CSV file
        writer.writerows(AllList)
    # At this point, the 'lines' list will contain all of the lines from the files