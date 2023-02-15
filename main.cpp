
//main 365
//while true 413
// filter 644

#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <stdio.h>
#include<thread>
#include <mutex>          // std::mutex
#include <queue>
//#include "stdafx.h"
#include <iostream>
#include <winsock2.h>
#include <WS2tcpip.h> //for SOCKET communication
#include <sstream>
#include <stdlib.h>
#include <fstream>
#include <iomanip>
#include "FileWriter.hpp"
#include <chrono>
#include "imageCollection.hpp"
#include "communicat.hpp"
#include "imageProcessing.hpp"
#include "main.hpp"
#include <limits>
#include <string>
#include "compileChoice.hpp"


#define maxAngleStep 58


#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")
#pragma warning(disable:4996)//to disable warning message

using namespace cv;
using namespace std;
using namespace std::this_thread; // sleep_for, sleep_until
using namespace std::chrono; // nanoseconds, system_clock, seconds


    float vinkel1Last=0;
    float vinkel2Last=0;
    float deltaTime=0;
    int ProcDeltaTimeInt=0;
int CurrState=0;
int LastState=0;
bool FrameSizeOk=false;
int ArdCmd1=0;
int ArdCmd2=0;
float position=0;
float testposition=0;

bool RecColl=false, RecProc=false, RecFil=false, RecComm=false;
bool OkCommColl=false, OkCommProc=false, OkCommFil=false, OkCommComm=false;
int OkCounterCommColl=0, OkCounterCommProc=0, OkCounterCommFil=0, OkCounterCommComm=0;
int specialcommand=0;
int tilProcCounter=0;
int fraCollCounter=0;
bool Connected=false;
float testAngle1=0;
float testAngle2=0;
int testCounter1=0;
int testCounter2=0;
bool firstLog=true;
float CurrAngle1=0;
float CurrAngle2=0;
int tester=0;
float testArray[40][6];
int PythonCmdGlobal=0;
InputFromOtherThreads communicator;


float linearinterpolate(float x1, float x2, float y1, float y2, float x)
{
    float y;
    y = y1 + (y2-y1)/(x2-x1)*(x-x1);
    return y;
}


float IIRfilter(float input, float lastOutput, float alpha)
{
    float output;
    output = alpha*input + (1-alpha)*lastOutput;
    return output;
}

int statemachine(int State, bool communicatCommonOk, int PythonCmd, bool CollRunning, bool ProcRunning, bool FrameSizeOki)
{
    #define StartSeq 3
    #define StopSeq 2
    #define StopAll 1
    
    int stateOut=State;
    switch (State)
    {
        case 0: // code to be executed if n = 1;
            if(OkCommComm)
            {
                stateOut=1;

            }
            break;
        case 1: // code to be executed if n = 1;
            if(OkCommColl && FrameSizeOki)
                stateOut=2;
            break;
        case 2: // code to be executed if n = 2;
            if(OkCommProc)
                stateOut=3;        
            break;
        case 3: // code to be executed if n = 2;
            if(OkCommFil)
            {
                stateOut=4;        

            }
            break;
        case 4: // standby;
            if(PythonCmd==StartSeq)
                stateOut=5;

            if(!communicatCommonOk || (PythonCmd==StopAll))
                stateOut=50;        
            break;


        case 5:
            if(CollRunning)
                stateOut=6;
            if(ProcRunning)
                stateOut=7;
            break;

        case 6:
            if(ProcRunning)
                stateOut=8;
            break;

        case 7:
            if(CollRunning)
                stateOut=8;
            break;

        case 8:
            if(PythonCmd==StopSeq)
                stateOut=9;
            break;

        case 9:
            communicator.stopRunning();
            stateOut=10;
            break;

        case 10:
            if(!ProcRunning)
            stateOut=4;
            break;


        case 50:
            if(!OkCommColl && !OkCommProc && !OkCommFil && !OkCommComm)
            stateOut=51;            
            break;

        case 51:
            stateOut=51;            
            break;


        default: // code to be executed if n doesn't match any cases
            cout << "Error, wrong state: " << State << endl;
            break;        
    }
    return(stateOut);
}


void CommOks()
{
    if (RecColl)
    {
        OkCounterCommColl=0;
        OkCommColl=true;
        RecColl=false;

    }
    else if (OkCommColl==true)
    {
        OkCounterCommColl++;
        if(OkCounterCommColl>2)
            OkCommColl=false;
    }

    if (RecProc)
    {
        OkCounterCommProc=0;
        OkCommProc=true;
        RecProc=false;
    }
    else if (OkCommProc==true)
    {
        OkCounterCommProc++;
        if(OkCounterCommProc>3)
        {
            OkCommProc=false;
            cout << "comm err proc" << endl;

        }
    }

    if (RecFil)
    {
        OkCounterCommFil=0;
        OkCommFil=true;
        RecFil=false;
    }
    else if (OkCommFil==true)
    {
        OkCounterCommFil++;
        if(OkCounterCommFil>2)
            OkCommFil=false;
    }

    if (RecComm)
    {
        OkCounterCommComm=0;
        OkCommComm=true;
        RecComm=false;
  
    }
    else if (OkCommComm==true)
    {
        OkCounterCommComm++;
        if(OkCounterCommComm>2)
            OkCommComm=false;
    }


}

int FloatToHalf(float f)
{
    int i = *(int*)&f;
    int sign = (i >> 16) & 0x8000;
    int val = (i & 0x7fffffff) + 0x1000;

    if (val >= 0x47800000) // might be or become NaN/Inf
    { // avoid Inf due to rounding
        if ((i & 0x7fffffff) >= 0x47800000)
        { // is or must become NaN/Inf
            if (val < 0x7f800000) // was value but too large
                return sign | 0x7c00; // make it +/-Inf
            return sign | 0x7c00 | // remains +/-Inf or NaN
                ((i & 0x007fffff) >> 13); // keep NaN (and Inf) bits
        }
        return sign | 0x7bff; // unrounded not quite Inf
    }

    if (val >= 0x38800000) // remains normalized value
        return sign | (val - 0x38000000) >> 13; // exp - 127 + 15
    if (val < 0x33000000) // too small for subnormal
        return sign; // becomes +/-0
    val = (i & 0x7fffffff) >> 23; // tmp exp for subnormal calc

    return sign | ((i & 0x7fffff | 0x800000) // add subnormal bit
        + (0x800000 >> val - 102) // round depending on cut off
        >> 126 - val); // div by 2^(1-(exp-127+15)) and >> 13 | exp=0
}


angleStuff angleAssement(float angle, float angleLast) //returnerer diff vinkel, og om den er ok
{
    angleStuff angleStuff;
// last 0 curr 359
    float ang1=angle - angleLast;
    float ang2=angle - angleLast + 360.0;
    float ang3=angle - angleLast - 360.0;
    
    float angleCurrent = 0;

    if (abs(ang1)<abs(ang2))
    {//ang1
        if(abs(ang1)<abs(ang3))
            angleCurrent=ang1;
        else
            angleCurrent=ang3;
    }
    else
    {//ang2 vs ang3
        if(abs(ang2)<abs(ang3))
            angleCurrent=ang2;
        else
            angleCurrent=ang3;
    }

    if(abs(angleCurrent)> maxAngleStep)
    {
        angleStuff.ok=false;
    }
    else
    {
        angleStuff.ok=true;
    }

    angleStuff.angle=angleCurrent;

    return angleStuff;
    //ctor
}


SendArray prepForSend2(ResultArray ProcessedData)
{

        int StatusToPyt=ProcessedData.array[0];

        float vinkel1=ProcessedData.array[1];
        float vinkel2=ProcessedData.array[2];
        float avstand=ProcessedData.array[3];
        
        float deltaV1=ProcessedData.array[4];
        float deltaV2=ProcessedData.array[5];
        float deltaPos=ProcessedData.array[6];
        int IDmarker=ProcessedData.array[7];
     



        SendArray send;

        int tmpint=StatusToPyt;
        send.array[0]=tmpint & 0xff;
        send.array[1]=tmpint >> 8 & 0xff;


//0 sts, 1 v1, 2 v2, 3  avst, 4 dv1, 5 dv2, 6 dvAvst, 7 id

        tmpint=FloatToHalf(vinkel1);
        send.array[2]=tmpint & 0xff;
        send.array[3]=tmpint >> 8 & 0xff;

        tmpint=FloatToHalf(vinkel2);
        send.array[4]=tmpint & 0xff;
        send.array[5]=tmpint >> 8 & 0xff;

        tmpint=FloatToHalf(avstand);
        send.array[6]=tmpint & 0xff;
        send.array[7]=(tmpint >> 8) & 0xff;

        tmpint=FloatToHalf(deltaV1);
        send.array[8]=tmpint & 0xff;
        send.array[9]=tmpint >> 8 & 0xff;

        tmpint=FloatToHalf(deltaV2);//deltaV1
        send.array[10]=tmpint & 0xff;
        send.array[11]=tmpint >> 8 & 0xff;

        tmpint=FloatToHalf(deltaPos);//deltaV2
        send.array[12]=tmpint & 0xff;
        send.array[13]=tmpint >> 8 & 0xff;


        tmpint=IDmarker;//
        send.array[14]=tmpint & 0xff;
        send.array[15]=tmpint >> 8 & 0xff;

    return(send);
}



int main(int, char**)
{


    // const char* corners_window = "Corners detected";

    thread th1(imgCollector);
    thread th2(localHostings); //thread th2(CommProc);
    thread th3(Measures);
    thread th4(FileWriter);

    sleep_for(seconds(1));
    auto OldTime = steady_clock::now();
    auto ElapsedT = steady_clock::now()-OldTime;
    int ProcErr=0;
    int ProcErrIntern=0;

    auto secondsy=duration_cast<milliseconds>(ElapsedT);
    auto secondsy2=duration_cast<milliseconds>(ElapsedT);
    long secCount=secondsy.count();    
    bool ProcRunning;
    int tmpRows=0;

    bool commPulseProc=false;
    bool commPulsepython=false;
    int commCountProc=0;
    int commCountpython=0;

    int logging=0;
    int loggingVerb=0;

    auto startColl = high_resolution_clock::now();;
    auto stopColl = high_resolution_clock::now();
    int timeTally=0;
    int tallyCounter=0;
    int MaindeltaTimeInt=0;
    int toPythCounter=0;
    int fromPythCounter=0;
int pgkID;
    float LastAngle1=0;
    float LastAngle2=0;
    float LastPos=0;
    int seccount2=0;
    int errprocCo=0;
    bool secPulse=false;
    bool ms20Pulse=false;
    float AccuAngl1=0;
    float AccuAngl2=0;  
    float AccuPos=0;
    auto LastTime=high_resolution_clock::now();
    int dataID20ms=0;
    int MainHz=0;
    int SampleCounter=0;
    bool AngleError=false;
    int testerCount=0;
    bool testTooHighnum=false;
    int testId=0;
    string tmpStringx="";
    auto timeStartRun=steady_clock::now();
    IDnStringArray tmpIDnStringArray;
    tmpIDnStringArray.pointer=0;
    tmpIDnStringArray.numElements=0;
    auto startAngleTimer = std::chrono::high_resolution_clock::now();
    auto stopAngleTimer = std::chrono::high_resolution_clock::now();

    while(true)
    {
        RecFil=true;
        MainHz++;
//-----------------------------------------------------test omløpstid--------------------------
        #if testPerf
            stopColl = high_resolution_clock::now();
            using ms = std::chrono::duration<float, std::milli>;
            deltaTime = std::chrono::duration_cast<ms>(stopColl - startColl).count();
            //cout<<fixed<<setprecision(5)<<deltaTime<<endl;

            startColl = high_resolution_clock::now();

            timeTally += int(deltaTime*10);

            tallyCounter++;
            if(tallyCounter>=30)
            {
//                                cout<<"heiehiehieih"<<endl;

                MaindeltaTimeInt=timeTally;
                timeTally=0;
                tallyCounter=0;
                
            }

        #endif




//-----------------------------------------------------sekund puls og sample puls -------------------------

        ElapsedT = steady_clock::now()-OldTime;

        secondsy=duration_cast<milliseconds>(ElapsedT);
        secCount=secondsy.count();
        secPulse=false;
        ms20Pulse=(secCount>=20);
        if(ms20Pulse)
        {
            OldTime = steady_clock::now();
            seccount2++;
            if(seccount2>=50)
            {
                secPulse=true;
                seccount2=0;
            }
        }

        if(secPulse)    
        {
            CommOks();
            OldTime = steady_clock::now();
            cout << "state: " << ( CurrState) << endl;//fjernes når vi kommer i gang
//            cout << "procerr: " << OkCounterCommProc << endl;//fjernes når vi kommer i gang

        //    cout << tmpRows << endl;
            commCountProc++;
            commCountpython++;
//            #cout<<fixed<<setprecision(5)<<deltaTime<<endl;
            #if testPerf
                cout << "main time: " <<  MainHz <<endl;
                cout << "proc time (1000iter i ms): " <<  ProcDeltaTimeInt <<endl;
                cout << "to python hz: " <<  toPythCounter <<endl;
                cout << "from proc hz: " <<  tilProcCounter <<endl;
                cout << "coll out hz: " <<  fraCollCounter <<endl;
                cout << "pyth out hz: " <<  fromPythCounter <<endl;
                cout << "cmd: " <<  PythonCmdGlobal <<endl;
                

                cout << endl;
                MainHz=0;
                fraCollCounter=0;
                tilProcCounter=0;
                toPythCounter=0;
         //       fromPythCounter=0;
                
            #endif

        }


        commPulseProc=secPulse && (commCountProc>1);
        commPulsepython=secPulse && (commCountpython>1);

        if(!OkCommProc && secPulse)
        {
            errprocCo++;
            if(errprocCo>15)
            {
                cout << (communicator.getLastPosProc()) << " :last pos--------------------------------" << endl;
            }
        }

//-----------------------------------------------------inn fra python--------------------------
        int PythonCmd;
        
        int ArdCmdTime1;
        int ArdCmdTime2;

        RecvArray mottattarr = communicator.DataCommMainPop(); //inn fra comm med python
        if(mottattarr.newitem)
        {
            #if (testPerf)
                if(pgkID== mottattarr.array[4])
                    ++fromPythCounter;
            #endif 
            
            PythonCmd=mottattarr.cmd;
            RecComm=true;
            ArdCmd1= mottattarr.array[1];
            ArdCmd2= mottattarr.array[2];

            
            pgkID= mottattarr.array[5];
            PythonCmdGlobal=PythonCmd;

        }


//-----------------------------------------------------inn fra collector--------------------------

        bool CollRunning;
        FrameTime FRTcollector=communicator.dataImgCollMainPop(); //inn fra collector
        if(FRTcollector.newitem)
        {
            
            //cout << inty << " :tid" << endl;
            

            CollRunning=((FRTcollector.CmdSts & 1)==1);
            RecColl=true;
            fraCollCounter++;

            if (FRTcollector.CmdSts & 2)
                FrameSizeOk=true;
            else
                FrameSizeOk=false;




            
        }

//-----------------------------------------------------ut til proc--------------------------

        if(FRTcollector.newitem || commPulseProc)// send data til PROC. 
        {
            
            //cout << "proccywoccy" << endl;
            
            FRTcollector.CmdSts=PythonCmd;
            //FRTcollector.IDs=
            if(!FRTcollector.newitem)
                cout << "trobbel her" << endl;
            if(FRTcollector.empty)
                cout << "trobbel her2" << endl;

            FRTcollector.empty = !FRTcollector.newitem || FRTcollector.empty;


            if((CurrState >= 6) || commPulseProc)
            {
               
                communicator.dataMainImgProcPush(FRTcollector);
                commCountProc=0;
            }
        }

        
//-----------------------------------------------------inn fra fil--------------------------

        WrtInfo FraWrt=communicator.dataWrtMainPop(); //fra fil
        if(FraWrt.newitem)
        {
            RecFil=true;
            if(FraWrt.stsCmd==1)
            {
                firstLog=false;

            }

        }
        
//-----------------------------------------------------inn fra proc--------------------------




        
        int myTmp=0;
        long duraCount=0;
        float deriv1=0;
        float deriv2=0;
        float deriPos=0;
        


        ResultArray ProcessedData =communicator.dataImgProcMainPop(); //fra image processing. b0 run sts:1-2 blå, osv til 9-10.  11 få pixel seed.
        ResultArray TilPythonArray ;
        if(ProcessedData.newitem)
        {
            tilProcCounter++;
            //cout << "proccywoccy" << endl;
            #if testPerf
                ProcDeltaTimeInt=ProcessedData.deltatime;
            #endif

            ProcRunning=ProcessedData.Sts & 1;
            RecProc=true;
            if(ProcessedData.empty)
                ProcErr=0b1000000000;
            else
                ProcErr=0;


            if(ProcessedData.Sts & 0b111111111110)
                ProcErr&=0b100000000;
            
            if((tester==ProcessedData.ID) && (ProcessedData.newitem))
                cout << "error 111" << endl;
            tester=ProcessedData.ID;






        }
        
//-----------------------------------------------------filtrer og downsample---------------------

        if(ProcessedData.newitem && !ProcessedData.empty)
        {



//            float IIRfilter(float input, float lastOutput, float alpha)AccuAngl2

            CurrAngle1=ProcessedData.array[0];// IIRfilter(ProcessedData.array[0], CurrAngle1, 0.3);
            CurrAngle2=ProcessedData.array[1];// IIRfilter(ProcessedData.array[1], CurrAngle2, 0.3); //indre




            angleStuff angleStuff1;
            angleStuff angleStuff2;

            angleStuff1=angleAssement(CurrAngle1,LastAngle1);
            angleStuff2=angleAssement(CurrAngle2,LastAngle2);

            if(SampleCounter<12)
            {
                AccuAngl1+=angleStuff1.angle;
                AccuAngl2+=angleStuff2.angle;
                SampleCounter++;
            }


            float leftMax=206;
            float rightMax=496;

            position= IIRfilter(linearinterpolate(leftMax,rightMax,-1.0,1.0,ProcessedData.array[2]), position, 0.3);

            
            if(!angleStuff1.ok || !angleStuff2.ok)
            {
                AngleError=true;
            }
            else
            {
                AngleError=false;
            }
            
            LastAngle1=CurrAngle1;
            LastAngle2=CurrAngle2;

            if(!testTooHighnum)
            {
                testArray[testerCount][0]=CurrAngle1;
                testArray[testerCount][1]=CurrAngle2;
                testArray[testerCount][2]=angleStuff1.angle;
                testArray[testerCount][3]=angleStuff2.angle;
                testArray[testerCount][4]=AccuAngl1;
                testArray[testerCount][5]=AccuAngl2;
                if(testerCount<39)
                    testerCount++;
                else
                    testerCount=0;

            }
            startAngleTimer = std::chrono::high_resolution_clock::now();
        }// TilPythonArray



        if(ms20Pulse)
        {//0 sts, 1 v1, 2 v2,3 avst, 4 dv1, 5 dv2, 6 dvAvst, 7 id
            stopAngleTimer = std::chrono::high_resolution_clock::now();
            auto durationAngl = std::chrono::duration_cast<std::chrono::microseconds>(stopAngleTimer - startAngleTimer);
            float durationAnglFloat=durationAngl.count()/20000.0;//justerer for at tidsramme ikke var akkurat 20ms
            CurrAngle1+=AccuAngl1*durationAnglFloat;
            CurrAngle2+=AccuAngl2*durationAnglFloat;

            //cout << "durationAnglFloat: " << durationAnglFloat << endl;
            //startAngleTimer = std::chrono::high_resolution_clock::now();

            dataID20ms++;

            deriv1=(AccuAngl1);
            deriv2=(AccuAngl2);
            deriPos=(position-AccuPos)*(10); //accupos= lastpos

            if(abs(deriv1)>999 || abs(deriv2)>999)
            {
                testTooHighnum=true;
                for (int i = 0; i < 40; i++)
                {
                    cout << testArray[i][0] << " :cv1 " << testArray[i][1] << " :cv2 " << testArray[i][2] << " :der1 der2:  " << testArray[i][3] << " " << testArray[i][4] << " :accu1 accu2: " << testArray[i][5] << endl;
                }
                cout << "deri1: " << deriv1 << " deri2: " << deriv2 << " accuangl1: " << AccuAngl1 << " accu2: " << AccuAngl2 << endl;
                getchar();
                testTooHighnum=false;
            }

            TilPythonArray.array[1]=CurrAngle1;
            TilPythonArray.array[2]=CurrAngle2;
            TilPythonArray.array[3]=position;
            TilPythonArray.array[4]=deriv1;
            TilPythonArray.array[5]=deriv2;
            TilPythonArray.array[6]=deriPos;
            TilPythonArray.array[7]=dataID20ms;

            LastPos=position;
            LastTime=ProcessedData.TimeFrame;
            AccuAngl1=0;
            AccuAngl2=0;
            AccuPos=0;
            AccuPos=position;

            SampleCounter=0;
        }


//-----------------------------------------------------ut til fil--------------------------
        if(PythonCmd==4)
            logging=true;

        int stopLogging=0;

        if(PythonCmd==5)
        {
            logging=false;
            stopLogging=2;
        }
        

        if(ms20Pulse && logging)
        {
            // auto cstamp=(steady_clock::now()-timeStartRun);
            // secondsy2=duration_cast<milliseconds>(cstamp);
            // long tg=secondsy2.count();
            
            tmpStringx +=   to_string(dataID20ms);
            tmpStringx += "," + to_string(ProcessedData.empty);
            tmpStringx += "," + to_string(ProcessedData.Sts) ;
            tmpStringx += "," + to_string(AngleError);

            tmpStringx +=  ","  + to_string(ProcessedData.array[0]); //v1
            tmpStringx +=  ","  + to_string(ProcessedData.array[1]); //v2
            tmpStringx +=  ","  + to_string(position);
            tmpStringx +=  ","  + to_string(deriv1);
            tmpStringx +=  ","  + to_string(deriv2);
            tmpStringx +=  ","  + to_string(deriPos);

                
        }

        if( mottattarr.newitem)//     må vente på cmd fra python før den logger.   commPulseProc ||
        {//logging && 
            string tmpString2;
            WrtInfo TilWrt;
            if(firstLog)
            {//

                tmpString2 = " incomID,id, empty-frame, sts, angel error, v1 (0-360), v2,  pos, dt-v1 (dgr pr sec), dt-v2, dt-pos (pct pr sec), act1 (raw), act2" ;



                tmpString2 += "\n";
                TilWrt.dataVerb=tmpString2;
            }
            string tmpString="";

            if(logging)
            {//int pgkID

                tmpString =  to_string(pgkID) + "," + tmpStringx ;
                tmpString +=  "," +  to_string(ArdCmd1);
                tmpString +=  "," +  to_string(ArdCmd2);

                tmpString += "\n";
                tmpStringx="";

                TilWrt.data=tmpString;//data, 3 vinkler, avst, derivat,comm err , id
            }


            TilWrt.stsCmd=logging | stopLogging;
        
           // cout << "herry: " + to_string(TilWrt.stsCmd) << endl;

            communicator.dataMainWrtPush(TilWrt);
        }





//-----------------------------------------------------ut til python--------------------------

        bool communicatCommonOk=OkCommComm && OkCommColl && OkCommProc && OkCommFil;

        if(ms20Pulse)
        {////0 sts, 1 v1, 2 v2,3 avst, 4 dv1, 5 dv2, 6 dvAvst, 7 id

            //logging  communicatCommonOk
            TilPythonArray.array[0]=CurrState | ProcErr | (communicatCommonOk<< 9) | (logging<< 10) | (OkCommProc << 11) | (AngleError << 12);

            SendArray sendPytData=prepForSend2(TilPythonArray); //data til python. sts: b0-7 cpp state. b8: common proc err, b9: empty.

            int fb=communicator.DataMainCommPush(sendPytData);// sender til python 
            commCountpython=0;      

            #if (testPerf)
                if(fb==0)
                    toPythCounter++;
            #endif      
        }
        

        
//-----------------------------------------------------FSM--------------------------

        
      
        CurrState=statemachine(CurrState, communicatCommonOk, PythonCmd, CollRunning, ProcRunning, FrameSizeOk);

        

    }


//-----------------------------------------------------The end-------------------------

    communicator.stopRunning();
    th1.join();
    th2.join();
    th3.join();
    th4.join();


    cout << "all done\n";

    getchar();
    return 1;

}
