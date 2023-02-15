#include "imageCollection.hpp"

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

//using namespace cv;
using namespace std;
#include <chrono>
#include "main.hpp"
#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")
#pragma warning(disable:4996)//to disable warning message
using namespace std::this_thread; // slesep_for, slesep_until
using namespace std::chrono; // nanoseconds, system_clock, seconds
#include "communicat.hpp"




extern InputFromOtherThreads communicator;


bool runnings=true;
void localHostings()
{
    WSADATA WSAData;

    SOCKET server, client;

    SOCKADDR_IN serverAddr, clientAddr;
    SendArray tmpsendarr;
    bool NewData=false;
    RecvArray ArrayMottatt;
    WSAStartup(MAKEWORD(2, 0), &WSAData);
    server = socket(AF_INET, SOCK_STREAM, 0);

    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(5555);
    ::bind(server, (SOCKADDR *)&serverAddr, sizeof(serverAddr));
    listen(server, 0);

    cout << "Listening for incoming connections..." << endl;
    int result;
    const int BUFFER_SIZE = 1024;
    char buffer[BUFFER_SIZE];
    int SecCounter=0;
//    string a_converted[1024];
    //memset(a_converted, 0, sizeof(a_converted));
    int clientAddrSize = sizeof(clientAddr);

    if ((client = accept(server, (SOCKADDR *)&clientAddr, &clientAddrSize)) != INVALID_SOCKET)
    {
        u_long mode = 1;  // 1 to enable non-blocking socket
        ioctlsocket(client, FIONBIO, &mode);
        cout << "Client connected!" << endl;
        //setConnected();
        
        // Loop 
        int i = 0;
        unsigned int ii = 0;//
        uint8_t iii=0;
        int IdInn=0;
        bool secpulse=false;
        int HzCount=0;
        while (communicator.getRunningComm()) {
            HzCount++;
            if(secpulse)
            {
                secpulse=false;
                cout << "Hz comm cpp: " << HzCount << endl;
                HzCount=0;
            }

// //#----------------------------mottar fra python-------------------------------------            
        // # dataOut[0]=cmd
        // # dataOut[1]=self.M1ActCommand
        // # dataOut[2]=self.M2ActCommand
        // # dataOut[3]=self.ActTimeVal1
        // # dataOut[4]=self.ActTimeVal2
        // # dataOut[5]=self.IDout

            int gg=recv( client, buffer, 1024, 0);  //receiving
            //char char_array[sizeof(a_converted)];
            bool newIncom=false;
            if ((gg == -1)) 
            {
                int ierr= WSAGetLastError();
                if(!(ierr==10035))
                {
                    printf("recv failed: %d\n", ierr);
                    printf("edrgg: %d\n",WSAEWOULDBLOCK);
                    runnings=false;
                    break;

                }
            }
            else
                newIncom=true;



            if(newIncom)
            {
                for (int i = 0; i <= 6; i++)
                {
                    
                    char oo1=buffer[i*2];
                    char oo2=buffer[i*2+1];
                    uint i1=oo1 & 0xff;
                    uint i2=oo2 & 0xff;
                    ii = i1 + (i2 * 256);//                ii=iii & 0xff;                
                    ArrayMottatt.array[i]=ii;
                //   cout << ArrayMottatt.array[i] << " " ;

                }

            //  cout  << endl;   

                ArrayMottatt.cmd=ArrayMottatt.array[0];
                // if(IdInn==ArrayMottatt.array[4])
                //     cout << "IdInn: lik lik -------------------------------------- " << IdInn << endl;
                IdInn=ArrayMottatt.array[5];
                communicator.DataCommMainPush(ArrayMottatt);
                NewData=false;

            }


            tmpsendarr=communicator.DataMainCommPop();
            NewData=tmpsendarr.newitem;
            if(!communicator.getRunningComm())
                break;


//#----------------------------sender til python-------------------------------------            

            char msg[16];
            if(NewData)
            {
                for (int ix = 0; ix <= 15; ix++)
                    msg[ix]=tmpsendarr.array[ix];

                int msg_len = 16;//strlen(msg);

                result=send(client, msg, msg_len, 0);   //sending

                SecCounter++;
                if(SecCounter>49)
                {
                    SecCounter=0;
                    secpulse=true;
                }
                else
                    secpulse=false;
            }



        }
        closesocket(client);
        WSACleanup();
        cout << "Client disconnected." << endl;
    }
    cout << "press enter" << endl;
}
