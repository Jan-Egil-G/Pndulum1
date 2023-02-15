void stopRunning();
bool getRunning();
void setConnected();
#include <queue>
#include <opencv2/core.hpp>
#include <iostream>
#include <chrono>

using namespace std::chrono; 

using namespace std;

#ifndef FrameTimeyx
#define FrameTimeyx

struct IDnString
{
    int ID;
    string data;
};

struct IDnStringArray
{
    IDnString array[10];
    int pointer;
    int numElements;
};

struct angleStuff
{
    float angle;
    bool ok;
};

struct RecvArray {
    int array[10];
    bool newitem;
    int cmd;
};
struct SendArray {
    char array[20];
    bool newitem=false;
    int Sts;
    bool empty;

};

#ifndef FrameTimey
#define FrameTimey

struct FrameTime 
{
    cv::Mat frme;
    std::chrono::time_point<std::chrono::high_resolution_clock>  TimeFrame;
    int IDs;
    bool newitem;
    int CmdSts;
    bool empty;
    
};

// your declarations (and certain types of definitions) here

#endif

using namespace cv;
struct ResultArray {
    float array[6];
    int ID;
    bool newitem;    
    int Sts;
    bool empty;
    int deltatime;
    std::chrono::time_point<std::chrono::high_resolution_clock>  TimeFrame;
};

struct WrtInfo
{
    int stsCmd;
    string data;
    string dataVerb;

    bool newitem;    

};

#endif

#ifndef inpOth
#define inpOth

class InputFromOtherThreads
{ // Private attributes access
  

private: // this line is not necessary, because fields declared
    std::queue<RecvArray> recvFIFOs;
    RecvArray mottattarr;
    std::mutex mtx1; 
    std::mutex mtx2; 
    std::mutex mtx3; 
    std::mutex mtx4; 
    std::mutex mtx5; 
    std::mutex mtx6; 
    std::mutex mtx7; 
    
    bool runningImg=true;
    bool runningMain=true;
    bool runningProc=true;
    bool runningFil=true;
    bool runningComm=true;
    
    bool connected=false;
    std::queue<FrameTime> CollectToMainQu;
    std::queue<FrameTime> MainToProcQu;
    std::queue<ResultArray> ProcToMainQu;
    std::queue<WrtInfo> MainToFileQu;
    std::queue<WrtInfo> FileToMainQu;
    
    std::queue<RecvArray> CommToMainQu;
    std::queue<SendArray> MainToCommQu;
    int CamNo=0;
    int possy=0;
    


// Attributes under this line can be accessed everywhere
public:

    // Class Method




    void dataMainImgProcPush(FrameTime input) 
    {
        


        mtx1.lock();
            if (MainToProcQu.size() > 5)
            {
                MainToProcQu.pop();
            }
            MainToProcQu.push(input);
        mtx1.unlock();
        return;

    }
    
    FrameTime dataMainImgProcPop()
    {
        FrameTime FTloc;
        mtx1.lock();
        if (MainToProcQu.size() > 0)
        {
            FTloc=MainToProcQu.front();
            MainToProcQu.pop();
            FTloc.newitem=true;
        }
        else
        {
            FTloc.newitem=false;
        }

        mtx1.unlock();
        return(FTloc);
    }


    void dataImgProcMainPush(ResultArray input)
    {
        mtx2.lock();
            if (ProcToMainQu.size() > 5)
            {
                ProcToMainQu.pop();
            }
            ProcToMainQu.push(input);
        mtx2.unlock();
        return;
    }

    ResultArray dataImgProcMainPop()
    {
        ResultArray results;
        results.Sts=0;
        mtx2.lock();
        if (ProcToMainQu.size() > 0)
        {
            results=ProcToMainQu.front();
            ProcToMainQu.pop();
            results.newitem=true;

        }
        else
        {
            results.newitem=false;
        }

        mtx2.unlock();
        return(results);
    }


    void dataMainWrtPush(WrtInfo input)//  vinkler tid pådrag feilkoder
    {
        mtx3.lock();
            if (MainToFileQu.size() > 5)
            {
                MainToFileQu.pop();
            }
            MainToFileQu.push(input);
        mtx3.unlock();
        return;

    }

    WrtInfo dataMainWrtPop()
    {
        WrtInfo stringToWrite;
        mtx3.lock();
        stringToWrite.newitem=false;
        if (MainToFileQu.size() > 0)
        {
            stringToWrite=MainToFileQu.front();
            MainToFileQu.pop();
            stringToWrite.newitem=true;
        }

        mtx3.unlock();
        return(stringToWrite);
    }                



//------------
    void dataWrtMainPush(WrtInfo input)//  vinkler tid pådrag feilkoder
    {
        mtx7.lock();
            if (FileToMainQu.size() > 5)
            {
                FileToMainQu.pop();
            }
            FileToMainQu.push(input);
        mtx7.unlock();
        return;

    }

    WrtInfo dataWrtMainPop()
    {
        WrtInfo FbToWrite;
        FbToWrite.newitem=false;
        mtx7.lock();
        if (FileToMainQu.size() > 0)
        {
            FbToWrite=FileToMainQu.front();
            FileToMainQu.pop();
            FbToWrite.newitem=true;
        }

        mtx7.unlock();
        return(FbToWrite);
    }  

//----------

    void dataImgCollMainPush(FrameTime newFrametime)
    {

        mtx4.lock();
            if (CollectToMainQu.size() > 5)
            {
                CollectToMainQu.pop();
            }
            CollectToMainQu.push(newFrametime);
        mtx4.unlock();
        return;

    }

    FrameTime dataImgCollMainPop()
    {
        FrameTime cropped_image;
        mtx4.lock();
        if (CollectToMainQu.size() > 0)
        {
            cropped_image=CollectToMainQu.front();
            CollectToMainQu.pop();
            cropped_image.newitem=true;
        }
        else
        {
            cropped_image.newitem=false;
            cropped_image.CmdSts=0;
        }

        mtx4.unlock();
        return(cropped_image);

    }      


    void DataCommMainPush(RecvArray input)
    {
        mtx5.lock();
            if (CommToMainQu.size() > 5)
            {
                CommToMainQu.pop();
            }
            CommToMainQu.push(input);
        mtx5.unlock();

        return;
    }


    RecvArray  DataCommMainPop()
    {
        RecvArray RecvData;
        mtx5.lock();
        if (CommToMainQu.size() > 0)
        {
            RecvData=CommToMainQu.front();
            CommToMainQu.pop();
            RecvData.newitem=true;
        }
        else
        {
            RecvData.newitem=false;
        }
        mtx5.unlock();
        return(RecvData); 
    }

    int DataMainCommPush(SendArray input)
    {
        mtx6.lock();
            int err=0;
            if (MainToCommQu.size() > 5)
            {   
                err=1;
                MainToCommQu.pop();
            }
            MainToCommQu.push(input);
        mtx6.unlock();
        return(err);
    }

    SendArray  DataMainCommPop()
    {
        SendArray  DataToSend;
        mtx6.lock();
        if (MainToCommQu.size() > 0)
        {
            DataToSend=MainToCommQu.front();
            MainToCommQu.pop();
            DataToSend.newitem=true;
        }
        else
        {
            DataToSend.newitem=false;
        }

        mtx6.unlock();
        return(DataToSend);
    }

   


    int GetCamNo()
    {
        return(CamNo);
    }


    void stopRunning()
    {
        cout << "stopp\n";
        cout << "stopp\n";

        bool runningImg=false;
        bool runningMain=false;
        bool runningProc=false;
        bool runningFil=false;
        bool runningComm=false;
    }



    bool getRunningImg()
    {
        return(runningImg);
    }

    bool getRunningMain()
    {
        return(runningMain);
    }

    bool getRunningProc()
    {
        return(runningProc);
    }

    bool getRunningFil()
    {
        return(runningFil);
    }

    bool getRunningComm()
    {
        return(runningComm);
    }


    void saveLastPosProc(int pos)
    {
        possy=pos;
        return;
    }


    int getLastPosProc()
    {
        return(possy);
    }


  
    // Constructor
    InputFromOtherThreads()
    {
    }


}; // Private attributes access
#endif



// int DataReceivedIn( RecvArray recvarr);


// RecvArray  DataReceivedOut();

