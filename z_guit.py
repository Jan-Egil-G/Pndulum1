
import time
import tkinter as tk
import threading
from tkinter import *
import random
from PIL import ImageTk, Image
#import PID

import agent

class Appy(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.endButton=False
        self.running=False
        self.Manual=False
   
        self.start()
        self.DictIndex=0
        self.Commy=None
        self.LetsPlot=False
        self.Deep=False
        self.onBreak=False
        self.Savey=False
        self.reward=0
        self.mode=0
        self.ping=False
        self.M1left=False
        self.M1right=False
        self.M2left=False
        self.M2right=False
        self.LogOn=False
        self.LogOff=False
        self.CountCmd=False
        self.MakeValset=False
        self.WriteWeight=False
        self.testFeatImp=False


        self.startCppComm=False
        self.stopCppComm=False
        self.specialCppComm=False

        self.CountCmd=False
        self.LagreLog=False
        self.PrepData=False
        self.FlushNorm=False
        self.TrainPhys=False
        self.DoPong=False
        self.FlushPong=False
        self.PlotPong=False
        self.TrainCtrl=False
        self.TestPhys=False
        self.TestCtrl=False
        self.PlotQ=False
        self.Comb=False

    def btnCount(self):
        self.CountCmd=True

    def btnLagreLog(self):
        self.LagreLog=True

    def btnPrepData(self):
        self.PrepData=True
    def btnFlushNorm(self):
        self.FlushNorm=True

    def btnTrainPhys(self):
        self.TrainPhys=True

    def btnTestPhys(self):
        self.TestPhys=True


    def btnPingPong(self): #manual
        self.DoPong=True


    def btnFlushPong(self): #pid
        self.FlushPong=True

    def btnPlotPong(self): #deep
        self.PlotPong=True

    def btnTrainCtrl(self): #pid
        self.TrainCtrl=True



    def btnTestCtrl(self): #pid
        self.TestCtrl=True

    def btnPlotQ(self): #pid
        self.PlotQ=True

    def btnComb(self): #pid
        self.Comb=True


    def btnPing(self): #pid
        self.ping=True

    def btnValSet(self): #
        self.MakeValset=True

    def btnWriWei(self): #
        self.WriteWeight=True

    def btntestFeatImp(self): #
        self.testFeatImp=True



    def callback(self):
        print("her ok")

        self.endButton=True

    def MakeCanvass(self, location,widthh=106, heighth=206,xi=80, yi=180,bgi="gray99"):
        canvass = tk.Canvas(location, width=widthh, height=heighth)  # Create 200x200 Canvas widget
        canvass.config(bg="gray99")
        canvass.place(x=xi, y=yi)

        return(canvass)

    def MakeValLabel(self,canvy,keyi, texti="None"):
        #text
        label1 = tk.Label(canvy,text=texti,fg="black", bg="white", width = 15)
        label1.pack()

        #value
        self.ValDict[keyi]=self.ValDict.pop(f"{self.DictIndex}vars")
        label2 = tk.Label(canvy,textvariable=self.ValDict[keyi],fg="black", bg="white", width = 15)
        label2.pack()
        self.DictIndex += 1

    def MakeRadioButtonsCanv(self,Id,nameArr, widthhi=130, heighthi=406,xii=680, yii=180,bgii="gray90"):
        canvy=self.MakeCanvass(self.root,widthh=widthhi, heighth=heighthi,xi=xii, yi=yii,bgi=bgii)
        # Create a variable to hold the unsigned integer value

        # Iterate over the bits in the binary string
        for i in range(16):

            gg1=IntVar()
            # Create a radiobutton for the bit IntVar() Checkbutton(root, text=nameArr[i], variable=gg1, onvalue=1, offvalue=0, height=5, width=20).pack()
            Checkbutton(canvy, text=nameArr[i], variable=gg1, onvalue=1, offvalue=0, height=1, width=20).pack()
            #tb.pack()
            self.n[Id].append(gg1)

    def SetRadiobuttons(self,Id, val):
        bin_str = bin(val)
        bit_list = [int(ch) for ch in bin_str[2:]]
        bit_list = [0] * (16 - len(bit_list)) + bit_list
        for i in range(0,8):
            
            self.n[Id][i].set(bit_list[i])

    def GetRadiobuttons(self,Id):
        bit_list = []
        for i in range(8,16):
            bit_list.append(self.n[Id][i].get())
        val = int("".join(str(i) for i in bit_list), 2)
        return val

    def SetRadiobuttonsInit(self,Id, val):
        bin_str = bin(val)
        bit_list = [int(ch) for ch in bin_str[2:]]
        bit_list = [0] * (16 - len(bit_list)) + bit_list
        for i in range(8,16):
            
            self.n[Id][i].set(bit_list[i])



    def MakeSlider(self,canvy,keyi, rangeTop=100,rangeBot=0):
        #value
        self.ValDict[keyi]=self.ValDict.pop(f"{self.DictIndex}vars")

        self.Slider = tk.Scale(canvy,variable=self.ValDict[keyi], from_=rangeTop, to=rangeBot, length = 175, tickinterval = 50)
        self.Slider.place(x = 0, y = 4)  
        self.DictIndex += 1

    def MakeCanvAndSngLabel(self, textii="None",widthhi=106, heighthi=206,xii=180, yii=180,bgii="gray90"):
        
        canvy=self.MakeCanvass(self.root,widthh=widthhi, heighth=heighthi,xi=xii, yi=yii,bgi=bgii)

        label1 = tk.Label(canvy,text=textii,fg="black", bg="white", width = 15)
        label1.pack()


    def MakeCanvAndLabel(self,keyii, textii="None",widthhi=106, heighthi=206,xii=180, yii=180,bgii="gray34"):
        
        canvy=self.MakeCanvass(self.root,widthh=widthhi, heighth=heighthi,xi=xii, yi=yii,bgi=bgii)
        lbl=self.MakeValLabel(canvy,keyii, texti=textii)
        
        


    def MakeCanvAndSlider(self,keyii,xii, yii,rangeTopi=100,rangeBoti=0):
        
        canvy=self.MakeCanvass(self.root,widthh=70, heighth=185,xi=xii, yi=yii+25,bgi="gray34")
        sld=self.MakeSlider(canvy,keyii,rangeTop=rangeTopi,rangeBot=rangeBoti)
        self.MakeCanvAndSngLabel( textii=keyii,widthhi=106, heighthi=206,xii=xii, yii=yii,bgii="gray90")
        

        
 
    def MakeLamp(self, keyi, xii, yii):
        canvy=self.MakeCanvass(self.root,widthh=21, heighth=21,xi=xii, yi=yii,bgi="gray34")            
        my_oval = canvy.create_oval(3, 3, 20, 20)  # Create a circle on the Canvas
      
        canvy.itemconfig(my_oval, fill="grey")
        self.LampDict[keyi] =canvy, my_oval
        
    def SetLamp(self, keyi, onoff):#"running"
        canvys, ovy = self.LampDict[keyi]
        if onoff:
            canvys.itemconfig(ovy, fill="green")        
        else:
            canvys.itemconfig(ovy, fill="grey")        


    def MakeEntryCanvLabel(self,  xii, yii,Textii,Textv):
        canvy=self.MakeCanvass(self.root,widthh=51, heighth=41,xi=xii, yi=yii+23,bgi="gray34")  
        Entr=Entry(canvy, width= 20,textvariable=Textv)
        Entr.pack()
        self.MakeCanvAndSngLabel( textii=Textii,widthhi=146, heighthi=206,xii=xii, yii=yii,bgii="gray90")



    def run(self):
        #root
        
        
        self.root = tk.Tk()
        self.strv1=tk.StringVar()
        self.strv2=tk.StringVar()
        self.strv3=tk.StringVar()
        self.strv4=tk.StringVar()
        self.strv5=tk.StringVar()
        self.strv6=tk.StringVar()
        self.strv7=tk.StringVar()
        self.strv8=tk.StringVar()
        self.strv9=tk.StringVar()
        self.strv10=tk.StringVar()
        self.strv11=tk.StringVar()
        self.strv2.set("0")
        self.var2=IntVar()

        self.n = [[],[]]  
        self.SliderLvlSetp=IntVar()
        self.SliderManSetp=IntVar()

        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("1000x670")
        self.baseVar=IntVar()
        self.ValDict={}
        for ii in range(40):
            self.ValDict[str(ii)+"vars"]=tk.IntVar()

        self.LampDict={}  

        #buttons
        TellButton = tk.Button(text="Count", command=self.btnCount)
        TellButton.place(x= 40, y =40)



        LagreLogButton = tk.Button(text="Save logs", command=self.btnLagreLog)
        LagreLogButton.place(x= 40, y =80)


        PrepDataButton = tk.Button(text="Prep Data", command=self.btnPrepData)
        PrepDataButton.place(x= 40, y =140)

        FlushNormButton = tk.Button(text="Flush norm", command=self.btnFlushNorm)
        FlushNormButton.place(x= 140, y =140)

        TrainPhysButton = tk.Button(text="Train phys", command=self.btnTrainPhys)
        TrainPhysButton.place(x= 40, y =180)

        TestPhysButton = tk.Button(text="Test phys", command=self.btnTestPhys)
        TestPhysButton.place(x= 40, y =220)



        PingPongButton = tk.Button(text="Do pong", command=self.btnPingPong)
        PingPongButton.place(x= 40, y =260)

        FlushPongButton = tk.Button(text="Flush pong", command=self.btnFlushPong)
        FlushPongButton.place(x= 140, y =260)

        PlotPongButton = tk.Button(text="Plot Q", command=self.btnPlotPong)
        PlotPongButton.place(x= 40, y =300)

        TrainCtrlButton = tk.Button(text="train ctrl", command=self.btnTrainCtrl)
        TrainCtrlButton.place(x= 40, y =340)

        TestCtrlButton = tk.Button(text="test ctrl", command=self.btnTestCtrl)
        TestCtrlButton.place(x= 40, y =380)

        PlotQButton = tk.Button(text="plot Q cur", command=self.btnPlotQ)
        PlotQButton.place(x= 40, y =420)

        comboButton = tk.Button(text="comb PNorm", command=self.btnComb)
        comboButton.place(x= 40, y =460)

        PingButton = tk.Button(text="Ping", command=self.btnPing)
        PingButton.place(x= 40, y =500)

        ValsetButton = tk.Button(text="mk Val set", command=self.btnValSet)
        ValsetButton.place(x= 40, y =540)

        writeWeiButton = tk.Button(text="write Wei", command=self.btnWriWei)
        writeWeiButton.place(x= 40, y =580)

        testFeatImpButton = tk.Button(text="test Feat Imp", command=self.btntestFeatImp)
        testFeatImpButton.place(x= 40, y =620)

        # self.SetLamp("Off", True)
        self.MakeEntryCanvLabel(  250, 20+50*0,"test log no",self.strv1)
        self.MakeEntryCanvLabel(  250,  20+50*1,"phys net sel",self.strv2)
        self.MakeEntryCanvLabel(  250,  20+50*2,"start line",self.strv3)
        self.MakeEntryCanvLabel(  250,  20+50*3,"stop line",self.strv4)
        self.MakeEntryCanvLabel(  250,  20+50*4,"learning rate",self.strv5)
        self.MakeEntryCanvLabel(  250,  20+50*5,"Batch size",self.strv6)
        self.MakeEntryCanvLabel(  250,  20+50*6,"Num Epocs",self.strv7)
        self.MakeEntryCanvLabel(  250,  20+50*7,"rand freq",self.strv8)
        self.MakeEntryCanvLabel(  250,  20+50*8,"Line Length",self.strv9)
        self.MakeEntryCanvLabel(  250,  20+50*9,"Num pred lines",self.strv10)
        self.MakeEntryCanvLabel(  250,  20+50*10,"Min q val",self.strv11)

        # self.MakeInputBox(self.root,keyi="None", texti="None")
        #labels with vals
        startPnt=50
        self.MakeCanvAndLabel(keyii="outCmdCpp", textii="Qv1",xii=480, yii=startPnt+50*0)
        self.MakeCanvAndLabel(keyii="angle1", textii="qv2",xii=480, yii=startPnt+50*1)
        self.MakeCanvAndLabel(keyii="Num_Pnorm", textii="Num_Pnorm",xii=480, yii=startPnt+50*2)
        self.MakeCanvAndLabel(keyii="Num_logs", textii="Num_logs",xii=480, yii=startPnt+50*3)
        self.MakeCanvAndLabel(keyii="Num_Norm", textii="Num_Norm",xii=480, yii=startPnt+50*4)
        self.MakeCanvAndLabel(keyii="Num_Pong", textii="Num_Pong",xii=480, yii=startPnt+50*5)




        #just label
        # self.MakeCanvAndSngLabel("Off", xii=750,yii=40)
        # self.MakeCanvAndSngLabel("Manual", xii=750,yii=70)
        # self.MakeCanvAndSngLabel("Inference", xii=750,yii=100)

        #slders
        # self.MakeCanvAndSlider("pwr",xii=240, yii=300,rangeTopi=100,rangeBoti=0)
        # self.MakeCanvAndSlider("time",xii=320, yii=300,rangeTopi=100,rangeBoti=0)
        # self.MakeCanvAndSlider("Random",xii=870, yii=3,rangeTopi=100,rangeBoti=0)

        name1=["spare","spare","","spare","train ctrl","Pong","train phys","prep data","spare","spare","spare","spare","LD ctrl chkp","LD phys chkp","BU ctrl chkp","BU phys chkp"] #cpp
        #name2=["err3","err4","","","","","","samband","","","","","spare","th2","inf contact","ardcom"]

        self.MakeRadioButtonsCanv(0,name1,xii=665, yii=50)
       # self.MakeRadioButtonsCanv(1,name2,xii=800, yii=250)


        canvassy = tk.Canvas(self.root, width=111, height=7)  # Create 200x200 Canvas widget
        canvassy.config(bg="black")
        canvassy.place(x=777, y=245)

        self.root.mainloop()