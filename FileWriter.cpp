//#include <filesystem>
#include <iostream>
using namespace std;
//using namespace std::chrono; 
#include "main.hpp"
#include<thread>
using namespace std::this_thread; // sleep_for, sleep_until
extern InputFromOtherThreads communicator;
#include <fstream> 
void openFile()
{

}
bool openError=false;
bool ClosedFile=false;
int FileCount=0;
bool state1Done=false;
bool state3Done=false;
string header;
int WriteCounter=0;
bool NewFileOpen=false;

int StateMachine(int State, int commandIn, bool pulse, bool NIpulse)
{
    
    int stateOut=State;

    switch (State)
    {
        case 0: // code to be executed if n = 1;
            if((commandIn == 1) && NIpulse)
            {
                
                stateOut=1;
                state1Done=false;
            }
            break;

        case 1: // åpne ny fil

            if(state1Done) 
                stateOut=2;
                WriteCounter=0;
            break;

        case 2: // skriver
            // if(pulse)
            //     WriteCounter++;
            if(WriteCounter>=1045)
            {
                stateOut=3;
                state3Done=false;
                WriteCounter=0;
            }
            break;

        case 3: // åpne ny fil

            FileCount++;
            if(state3Done)
                stateOut=1;

            break;


        default: // code to be executed if n doesn't match any cases
            cout << "Error, wrong state: " << State << endl;
            break;  


    }

    return(stateOut);
}



void FileWriter()
{

    WrtInfo infoToMain;

    bool wrtPulse=false;
    int CurrState=0;
    ofstream myfile;
    for(;;)
    {
           // sleep_for(milliseconds(10));
        if(CurrState==1)
        {
            myfile.open("C:/PyPj/doublepend2/LogDir/Logs/Log_" + to_string(FileCount) + ".csv",fstream::out);
            myfile.close();
            myfile.open("C:/PyPj/doublepend2/LogDir/Logs/Log_" + to_string(FileCount) + ".csv",std::ios_base::app);
            if(!myfile.is_open())
            {
                openError=true;
                cout << "open -------------------error\n";
            }
            else
            {
                state1Done=true;
                NewFileOpen=true;
            }
        }

        if(CurrState==3)
        {
            myfile.close();
            state3Done=true;
        }

        wrtPulse=false;
        WrtInfo incomingData=communicator.dataMainWrtPop();
        if(incomingData.newitem)
        {
            if(header=="")
            {
                if (incomingData.dataVerb == "")
                {
                    header="missing"; //infoToMain
                    infoToMain.stsCmd=2;
                }
                else
                {
                    header=incomingData.dataVerb;
                    infoToMain.stsCmd=1;

                }
            }

            //cout << incomingData.stsCmd << "  :sts" << CurrState<< " :st  cnt: "<<WriteCounter<< "\n";// std::filesystem::remove_all("C:/PyPj/doublepend2/testdir");
            if(!openError && !ClosedFile  && (incomingData.stsCmd == 1))
            {
                if (CurrState==2)
                {
                    if(NewFileOpen)
                    {
                        myfile << header ;
                        NewFileOpen=false;
                    }

                    myfile << incomingData.data; 
                    
                    WriteCounter++;
                    wrtPulse=true;
                }

            }

            if(incomingData.stsCmd == 2)
            {
                ClosedFile=true;
            }
            
        }


        CurrState=StateMachine(CurrState,incomingData.stsCmd,wrtPulse,incomingData.newitem);
        wrtPulse=false;




        if(ClosedFile)
        {
            if(myfile.is_open())
                myfile.close();
        }



        if(incomingData.newitem )
        {
            communicator.dataWrtMainPush(infoToMain);
        }
    }
}

