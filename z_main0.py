
import z_guit
import z_prepareData
import time
import z_fileoperations
import z_CommonFunc as zcf
import os
import z_TrainPhys
import z_pong
import z_ping

import z_TrainCtrl

if __name__ == '__main__':
    app2 = z_guit.Appy()


import matplotlib.pyplot as plt  
  
def flatten(t):
    return [item for sublist in t for item in sublist]
    
class mainTrain:
    def __init__(self):    
        self.numLogs=0
        self.numNorms=0 
        self.numPreNorms=0
        self.numPongs =0
        self.PrepInProgress=False
        self.PrepCount=0
        self.radioval=0
        self.Testlog=1
        self.PhysNeuralNetSelected=1
        self.stopline=99999
        self.startline=1
        self.LRhigh=0.0001
        self.Batchsize=110
        self.Epochs=6
        self.randFreq=4
        self.linelength=10
        self.linecount=3
        self.TrphyInProgress=False
        self.TrphyCount=0
        self.PongInProgress=False
        self.PongCount=0
        self.CtrlInProgress=False
        self.CtrlCount=0
        self.qlist=[]
        self.MinQval=15.0


    def TurnOffProgress(self):
        if(self.PrepInProgress):
            self.PrepCount+=1
            if(self.PrepCount>20):
                self.PrepInProgress=False
                self.PrepCount=0

        if(self.TrphyInProgress):
            self.TrphyCount+=1
            if(self.TrphyCount>20):
                self.TrphyInProgress=False
                self.TrphyCount=0

        if(self.PongInProgress):
            self.PongCount+=1
            if(self.PongCount>20):
                self.PongInProgress=False
                self.PongCount=0

        if(self.CtrlInProgress):
            self.CtrlCount+=1
            if(self.CtrlCount>20):
                self.CtrlInProgress=False
                self.CtrlCount=0

    def testfileFolder(self,path, filestubBegin,filestubEnd):#0 based
        fileCount=0
        for i in range(9000):

            if(os.path.exists(path + filestubBegin + str(i) + filestubEnd)):
                fileCount+=1
            else:
                break
        return fileCount


    def testFiles(self):
        
        numLogs=self.testfileFolder("./LogDir/Logs/", "Log_",".csv")
        numPreNorms=self.testfileFolder("./LogDir/prenorm/", "Log_",".csv")
        numNorms=self.testfileFolder("./LogDir/norm/", "Log_",".csv")
        numPongs=self.testfileFolder("./LogDir/pingpong/", "Log_",".csv")
        
        return numLogs,numPreNorms, numNorms, numPongs



    def getRadiobutton(self,bit):
        mask = 1 << bit
        rva=app2.GetRadiobuttons(0)
        return (rva & mask) != 0

    def SetButtonRadio(self, bit, value):
        mask = 1 << (bit + 8)
        if(value): #turn on
            self.radioval |= mask
        else: #turn off
            self.radioval &= ~mask
        #print(self.radioval)
        app2.SetRadiobuttons(0,self.radioval)#


    def validatePosFloat(self, strval):
        str=strval.get()
        try:
            val = float(str)
            if val <= 0:
                strval.set("0.0001")
                return 0.0001
            else:
                return val
        except ValueError:
            strval.set("0.0001")
            return 0.0001


    def validatePosNumZ(self, strval,orgNum):
        str=strval.get()
        try:
            val = int(str)
            if val < 0:
                strval.set(orgNum)
                return orgNum
            else:
                return val
        except ValueError:
            strval.set(orgNum)
            return orgNum


    def validatePosNum(self, strval,orgNum):
        str=strval.get()
        try:
            val = int(str)
            if val < 1:
                strval.set(orgNum)
                return orgNum
            else:
                return val
        except ValueError:
            strval.set(orgNum)
            return orgNum

    def UpdateGui(self):
        if(app2.CountCmd):

            app2.CountCmd=False        
            self.numLogs, self.numPreNorms, self.numNorms, self.numPongs=self.testFiles()
            app2.strv2.set(str(self.numLogs-1))

        if(app2.LagreLog):
            app2.LagreLog=False
            z_fileoperations.saver()

        if(app2.PrepData): #prep data
            app2.PrepData=False
            self.PrepInProgress=True
            self.SetButtonRadio(0, True)
            z_prepareData.PrepData()

        if(app2.TrainPhys):
            app2.TrainPhys=False
            self.TrphyInProgress=True
            self.SetButtonRadio(1, True)
            ldchkp=self.getRadiobutton(2)

            z_TrainPhys.trainphys1(self.PhysNeuralNetSelected,self.Epochs,self.Batchsize,self.LRhigh,ldchkp,self.startline,
            self.stopline,testing=False,batchgroup=50)





        if(app2.TestPhys):
            app2.TestPhys=False

            z_TrainPhys.trainphys(1,1,0,True,self.startline,self.stopline,True)


        if(app2.DoPong):
            app2.DoPong=False
            self.SetButtonRadio(2, True)
            self.PongInProgress=True
            self.qlist=z_pong.pong(self.MinQval,self.linecount,self.randFreq,self.linelength,self.startline,self.stopline)
        
        if(app2.PlotPong):
            app2.PlotPong=False
            
            zcf.plotbar(flatten(self.qlist))

        if(app2.FlushNorm):
            app2.FlushNorm=False
            print("flush")
            z_fileoperations.delete_content()

        if(app2.TrainCtrl):
            app2.TrainCtrl=False
            self.SetButtonRadio(3, True)
            self.CtrlInProgress=True
            ldchkp=self.getRadiobutton(3)
            print("step1")
            addnoise=self.getRadiobutton(5)
            z_TrainCtrl.train_model_ctrl(self.Epochs,self.Batchsize,self.LRhigh,self.numPongs,ldchkp,-1,self.startline,self.stopline,addnoise)

        if(app2.TestCtrl):
            app2.TestCtrl=False

            z_TrainCtrl.train_model_ctrl(1,1,0.0,0,True,self.Testlog,self.startline,self.stopline)


        if(app2.PlotQ):
            app2.PlotQ=False
            zcf.plotQcurves(True)

        if(app2.Comb):
            app2.Comb=False
            z_fileoperations.combine(self.numLogs-1)#nummeret til siste logg

        if(app2.ping):
            app2.ping=False
            
            self.qlist=z_ping.ping(self.MinQval,self.linelength,self.Testlog,self.startline,self.stopline)

        if(app2.MakeValset):
            app2.MakeValset=False
            z_fileoperations.MakeTestSet(self.startline,self.stopline)
        
        if(app2.WriteWeight):
            app2.WriteWeight=False
            z_TrainPhys.printWeightsToCsv(self.PhysNeuralNetSelected)


        if(app2.testFeatImp):
            app2.testFeatImp=False
            res=z_TrainPhys.featureImportancePermutation(self.PhysNeuralNetSelected,self.Batchsize,self.startline,self.stopline)
            print(res)




        app2.ValDict["Num_logs"].set('{number:.{digits}f}'.format(number=self.numLogs, digits=0))# comment
        app2.ValDict["Num_Norm"].set('{number:.{digits}f}'.format(number=self.numNorms, digits=0))# comment
        app2.ValDict["Num_Pong"].set('{number:.{digits}f}'.format(number=self.numPongs, digits=0))# comment
        app2.ValDict["Num_Pnorm"].set('{number:.{digits}f}'.format(number=self.numPreNorms, digits=0))# comment



   
        dd=app2.GetRadiobuttons(0)
        self.SetButtonRadio(0, self.PrepInProgress)
        self.SetButtonRadio(1, self.TrphyInProgress)
        self.SetButtonRadio(2, self.PongInProgress)
        self.SetButtonRadio(3, self.CtrlInProgress)

        #entries
        self.Testlog=self.validatePosNumZ(app2.strv1,self.Testlog)#startlog
        self.PhysNeuralNetSelected=self.validatePosNumZ(app2.strv2,self.PhysNeuralNetSelected)#endlog
        self.startline=self.validatePosNum(app2.strv3,self.startline)#stopline
        self.stopline=self.validatePosNum(app2.strv4,self.stopline)#lr low
        self.LRhigh=self.validatePosFloat(app2.strv5)#lr high
        self.Batchsize=self.validatePosNum(app2.strv6,self.Batchsize)#Batchsize
        self.Epochs=self.validatePosNum(app2.strv7, self.Epochs)#Epochs
        self.randFreq=self.validatePosNum(app2.strv8,self.randFreq)#Rand freq
        self.linelength=self.validatePosNum(app2.strv9,self.linelength)#linelength
        self.linecount=self.validatePosNum(app2.strv10,self.linecount)#num pred lines pr starting point
        self.MinQval=self.validatePosFloat(app2.strv11)#num pred lines pr starting point





    #os.path.exists(f'./LogDir/norm/Log_{i}.csv')

if __name__ == '__main__':
    trainer=mainTrain()
    time.sleep(1)
    app2.SetRadiobuttonsInit(0, 12)
    while(True):
        
        time.sleep(0.1)
        trainer.UpdateGui()
        if(app2.specialCppComm):

            app2.specialCppComm=False


            # creating the dataset 
            data = {'C':20, 'C++':15, 'Java':30,  
                    'Python':35} 
            courses = list(data.keys()) 
            values = list(data.values()) 
            

            fig = plt.figure(figsize = (5, 5)) 
            
            # creating the bar plot 
            plt.bar(courses, values, color ='green',  
                    width = 0.4) 
            
            plt.xlabel("Courses offered") 
            plt.ylabel("No. of students enrolled") 
            plt.title("Students enrolled in different courses") 
            plt.show() 
        trainer.TurnOffProgress()

        EndProgram=app2.endButton
        if(EndProgram):
            print("end")
            app2.root.quit()
            break

print("gogohome")
