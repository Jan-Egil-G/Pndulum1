
import tkinter as tk
import threading
from tkinter import *
#import PID


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

        self.M1left=False
        self.M1right=False
        self.M2left=False
        self.M2right=False
        self.LogOn=False
        self.LogOff=False


        self.startCppComm=False
        self.stopCppComm=False
        self.specialCppComm=False



    def btnctrlMode(self):
        self.mode+=1
        if(self.mode>2):
            self.mode=0
        if(self.mode==0):
            self.SetLamp("Off", True)
            self.SetLamp("Inference", False)
            self.SetLamp("Manual", False)
        if(self.mode==1):
            self.SetLamp("Off", False)
            self.SetLamp("Inference", False)
            self.SetLamp("Manual", True)
        if(self.mode==2):
            self.SetLamp("Manual", False)
            self.SetLamp("Off", False)
            self.SetLamp("Inference",True )

    def btnStop(self):
        self.running=False
        self.SetLamp("running", False)

    def btnComOn(self):
        self.startCppComm=True

    def btnComOff(self):
        self.stopCppComm=True


    def btnLoad(self): #manual
        print("specialllllll")
        self.specialCppComm=True


    def btnM1left(self): #pid
        self.M1left=True
        print("gogo")

    def btnM1right(self): #deep
        self.M1right=True
        print("gogo")

    def btnM2left(self): #pid
        self.M2left=True

    def btnM2right(self): #deep
        self.M2right=True

    def btnLogOn(self): #deep
        
        self.LogOn=True

    def btnLogOff(self): #deep
        self.LogOff=True






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
        for i in range(16):
            
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






    def run(self):
        #root
        
        self.root = tk.Tk()
        self.var2=IntVar()
        self.n = [[],[]]  
        self.SliderLvlSetp=IntVar()
        self.SliderManSetp=IntVar()

        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("1000x670")
        self.baseVar=IntVar()
        self.ValDict={}
        for ii in range(30):
            self.ValDict[str(ii)+"vars"]=tk.IntVar()

        self.LampDict={}  

        #buttons
        StartButton = tk.Button(text="ctrlMode", command=self.btnctrlMode)
        StartButton.place(x= 650, y =40)






        LoadButton = tk.Button(text="Start", command=self.btnLoad)
        LoadButton.place(x= 40, y =120)


        M1leftButton = tk.Button(text="m1 left", command=self.btnM1left)
        M1leftButton.place(x= 100, y =320)
        M1RightButton = tk.Button(text="m1 right", command=self.btnM1right)
        M1RightButton.place(x= 100, y =350)

        M2leftButton = tk.Button(text="m2 left", command=self.btnM2left)
        M2leftButton.place(x= 180, y =320)
        M2RightButton = tk.Button(text="m2 right", command=self.btnM2right)
        M2RightButton.place(x= 180, y =350)



        LogOnButton = tk.Button(text="log on", command=self.btnLogOn)
        LogOnButton.place(x= 40, y =220)
        LogOffButton = tk.Button(text="log off", command=self.btnLogOff)
        LogOffButton.place(x= 40, y =250)


    

        self.MakeLamp("Off", 720, 40)
        self.MakeLamp("Manual", 720, 70)
        self.MakeLamp("Inference", 720, 100)


        self.SetLamp("Off", True)



        #labels with vals
        startPnt=80
        self.MakeCanvAndLabel(keyii="outCmdCpp", textii="command",xii=480, yii=startPnt+50*0)
        self.MakeCanvAndLabel(keyii="angle1", textii="angle1 ytre",xii=480, yii=startPnt+50*1)
        self.MakeCanvAndLabel(keyii="angle2", textii="angle2 indre",xii=480, yii=startPnt+50*2)
        self.MakeCanvAndLabel(keyii="angle1Dt", textii="angle1Dt ytre",xii=480, yii=startPnt+50*3)
        self.MakeCanvAndLabel(keyii="angle2Dt", textii="angle2Dt indre",xii=480, yii=startPnt+50*4)
        self.MakeCanvAndLabel(keyii="CppState", textii="cpp state",xii=480, yii=startPnt+50*5)
        self.MakeCanvAndLabel(keyii="Py_State", textii="Py_State",xii=480, yii=startPnt+50*6)
        self.MakeCanvAndLabel(keyii="HzIn", textii="HzIn",xii=480, yii=startPnt+50*7)
        self.MakeCanvAndLabel(keyii="VognPos", textii="VognPos",xii=480, yii=startPnt+50*8)
        self.MakeCanvAndLabel(keyii="pos DV", textii="pos DV",xii=480, yii=startPnt+50*9)
        
        

        #just label
        self.MakeCanvAndSngLabel("Off", xii=750,yii=40)
        self.MakeCanvAndSngLabel("Manual", xii=750,yii=70)
        self.MakeCanvAndSngLabel("Inference", xii=750,yii=100)

        #slders
        self.MakeCanvAndSlider("pwr",xii=240, yii=300,rangeTopi=100,rangeBoti=0)
        self.MakeCanvAndSlider("time",xii=320, yii=300,rangeTopi=100,rangeBoti=0)
        self.MakeCanvAndSlider("Random",xii=870, yii=3,rangeTopi=100,rangeBoti=0)

        name1=["err1","err2","","angle error","proc comm","logg","comm intern","proc err","spare","spare","spare","spare","spare","spare","spare","spare"] #cpp
        name2=["err3","err4","","","","","","samband","","","","","spare","th2","inf contact","ardcom"]

        self.MakeRadioButtonsCanv(0,name1,xii=665, yii=250)
        self.MakeRadioButtonsCanv(1,name2,xii=800, yii=250)




        self.root.mainloop()