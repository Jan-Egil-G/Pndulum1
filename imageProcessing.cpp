#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include <iostream>
#include <fstream>
#include <math.h>  
#include <chrono> 
#include <thread>
#include <chrono> 
#include <iostream>

#include "main.hpp"
#include "imageProcessing.hpp"
#include "main.hpp"
#include "compileChoice.hpp"
#include <ctime>

using namespace std;
using namespace std::chrono; 
using namespace std::this_thread; // sleep_for, sleep_until

#define blue 1
#define green 2
#define red 3
#define yellow 4
#define yellowR 5
#define PI 3.14159265    
#define inRangy(a, x, b) ((a<x) && (x<b))
#define startRun 3
#define stopRun 2

using namespace std::chrono; 
using namespace cv;
using namespace std;

Mat src, src_gray, dst_norm_scaled;
Mat dst_norm;
bool debuggy=false;
int debugCounter1=0;
RNG rng(12345);

int center[2];

int resultatSts=0;
const char* source_window = "Source image";
int groupedNumber=0;
bool firstRunni = true;
void funkys(void);

int antFoerRefine=0;

Vec3b mineo1;
Vec3b mineo2;
Vec3b mineo3;


ofstream myfile;
extern InputFromOtherThreads communicator;


int colorpixarray[50][6][2]; //holder med tre, må fixe index 13 > 02
float resultat[5];
int counters[7];

bool blockArray[750][500];



//e(360,240));
int stride=0;    
int CornTop=110; //top:0, bottom: 240
int CornLeft=30;
int CornRight=300;
int MaxSeedPix=35;
int MinBluePix=10;
int MinGreenPix=10;
int MinRedPix=10;
int MinCornLpix=3;
int MinCornRpix=3;

int MinPixNumber=35;
int MaxPixNumber=1999;
int MaxToBeProcOneColor=790;
#define SizeOfProcArray 800


// ResultArray Measures(int gogo, Mat img)
int teller=0;
void Measures()
{
    FrameTime incomData;
    incomData.newitem=false;        
    int seqRunning=0;


    auto startColl = high_resolution_clock::now();;
    auto stopColl = high_resolution_clock::now();
    int timeTally=0;
    int tallyCounter=0;
    int ProcdeltaTimeInt=0;
    float deltaTime=0;
    while(communicator.getRunningProc())
    {
        
   
        if (smallImg)
        {
            stride = 3;
                //corner exception
            CornTop=110;
            CornLeft=30;
            CornRight=300;

        }
        else
        {
            stride = 4;    
            CornTop=300;
            CornLeft=50;
            CornRight=600;

        }



        incomData=communicator.dataMainImgProcPop();



        if (!incomData.newitem)
        {

            continue;

        }

        incomData.newitem=false;
        //seqRunning=1;

        if(incomData.CmdSts>0)
        {
            if(incomData.CmdSts==startRun)
            {
                seqRunning=1;

            }

            if(incomData.CmdSts==stopRun)
            {
                seqRunning=0;
            }

        }
        ResultArray rr;
        rr.TimeFrame=incomData.TimeFrame;

        int tmpSts=seqRunning;

        if(incomData.empty)
        {

            rr.Sts =resultatSts | seqRunning;
            rr.empty = true;
            communicator.dataImgProcMainPush(rr);
            cout << "her pa empty" << endl;
            continue;
        }
        
        
        rr.Sts =resultatSts | seqRunning;
        //rr.Sts = 13;
        if(seqRunning)
        {
            #if testPerf
                startColl = high_resolution_clock::now();
            #endif
            rr.empty = false;
            src =  incomData.frme.clone();//imread("C:\\dne3.png", IMREAD_COLOR);

            groupedNumber=0;
            funkys();

            rr.array[0]=resultat[0];
            rr.array[1]=resultat[1];
            rr.array[2]=resultat[2];
            rr.array[3]=resultat[3];
            
            //int tmpSts2=resultat[3];
            rr.ID=incomData.IDs;
            #if slowdown
                sleep_for(milliseconds(100));
            #endif


            #if testPerf
                stopColl = high_resolution_clock::now();
                using ms = std::chrono::duration<float, std::milli>;
                deltaTime = std::chrono::duration_cast<ms>(stopColl - startColl).count();

                timeTally += int(deltaTime*10);
                tallyCounter++;
                if(tallyCounter>=30)
                {
                    ProcdeltaTimeInt=timeTally;
                    timeTally=0;
                    tallyCounter=0;
                }
                rr.deltatime=int(deltaTime*1000);//ProcdeltaTimeInt;

            #endif


          //  rr.Sts = 12;
        }
        else
            rr.empty = true;
    
        communicator.dataImgProcMainPush(rr);
    }
   
}


int getColor(Vec3b colorIn)
{
    int colorBack=0;
    int blueVal = colorIn[0];
    int greenVal = colorIn[1];
    int redVal = colorIn[2];
    
    // if(blueVal>45)
    // {
    //     cout << "holllo!" << colorIn << endl;
    //     getchar();
    // }

    if((blueVal >190)&& (redVal <60) && ((blueVal-greenVal) > 45) )
        colorBack=blue;
    
    if((greenVal >200) && (redVal <50) && ((greenVal-blueVal) > 19) )
        colorBack=green;

    if((blueVal< 40) && (greenVal <40) && (redVal >205))
        colorBack=red;

    if((colorBack==0) && ((blueVal< 95) && (greenVal >70) && (redVal >122)))
    {
        colorBack=yellow;


    }

    // if((blueVal< 80) && (greenVal >80) && (redVal >80))
    //     colorBack=yellow;


    return (colorBack);
}


void tegnsirkel(int x, int y)
{
    int xx=x;
    int yy=y;
    Point center(yy , xx);
    circle(src, center, 4, Scalar(rng.uniform(0,255), rng.uniform(0, 256), rng.uniform(0, 256)), FILLED );   

}


void SirkelFraArray(cv::Mat &bilde, int points[100][2])
{

    int endofpoints=groupedNumber;//points[99][0];
    for( int i = 0; i < endofpoints ; i++ )
    {
        //cout << "go";
        int xx=points[i][0];
        int yy=points[i][1];
        Point centert(xx , yy);
        circle( bilde, centert, 4, Scalar(rng.uniform(0,255), rng.uniform(0, 256), rng.uniform(0, 256)), FILLED );        
    }

}

void SirkelFraPt(cv::Mat &bilde, int point[2])
{

    int xx=point[0];
    int yy=point[1];
    Point center(xx , yy);
    circle( bilde, center, 4, Scalar(rng.uniform(0,255), rng.uniform(0, 256), rng.uniform(0, 256)), FILLED );        

}
float vinkel(int pts[2],int ptp[2])
{


   // double result = atan2 (ptp[1]-pts[1],ptp[1]-pts[0]) * 180 / PI;

   float param, ptop, tbunn, result;
    if((ptp[0]-pts[0])==0)
    {
        if((ptp[1]-pts[1])>0)
        {

            return(270.0);
        }
        else
            return(90.0);
    }

    bool xpos=((ptp[0]-pts[0])>=0);
    bool ypos=((pts[1]-ptp[1])>=0); //  pos y i første kvadrant

    

    ptop = (pts[1]-ptp[1]); //  pos y i første kvadrant
    tbunn = (ptp[0]-pts[0]); // pos x
    param =ptop/tbunn;


    result = atan (param) * 57.3;//180 / PI;

    if (result < 0)
        result += 90;

    if (xpos)
    {
        if ( !ypos)
        {
            
          //  printf( "%6.4lf", result ); 

            result +=270.0;

        }
    }
    else
    {
        if (ypos)
            result +=90.0;
        else
            result +=180.0;

    }


return result;
}



int PointDistance(int point1[2], int point2[2])
{
    int fac1 = (point1[0]-point2[0]);
    int fac2 = (point1[1]-point2[1]);
    
    return (fac1*fac1+fac2*fac2);
    
}


bool findColorPix(int rowwy, int colly) //finner "seed-pixler" som senere skal brukes til å finne hele flater
{


    int i = 0;


    counters[0]=0;
    counters[1]=0;
    counters[2]=0;
    counters[3]=0;
    counters[4]=0;
    counters[5]=0;




    while(  i < colly )//går gjennom alle pixler. 0-360 smallimg
    {
        int j = 0;
        while(  j < rowwy)//0-240 smal img
        {
            int xx=i;
            int yy=j;

            mineo1=src.at<Vec3b>(yy, xx); // y, x
            int colorFB= getColor(mineo1);
            if((yy>CornTop) && (xx>CornRight))//høyre hjørne  
            {

                if(colorFB==yellow)
                {
                    colorFB=5;//høyre hjørne


                }
            }
         
            if(colorFB>0) //hvis det er en farge
            {
                if(counters[colorFB] < MaxSeedPix) //max 45 seed-pixler
                {
                    colorpixarray[counters[colorFB]][colorFB][0]=xx;
                    colorpixarray[counters[colorFB]][colorFB][1]=yy;

                    counters[colorFB]++;
                    if(counters[colorFB] > 49)
                    {
                        cout << "----------------too many" << endl;
                        
                    }

                }
            }


            j+=stride;        
        }

        i+=stride;        
    }


    if((counters[1]<MinBluePix) || (counters[2]<MinGreenPix) || (counters[3]<MinRedPix) || (counters[4]<MinCornLpix) || (counters[5]<MinCornLpix))
    {
        cout << "too little, BGR LCRC: " << counters[1] << " "  << counters[2] << " "  << counters[3] << " "  << counters[4] << " " << counters[5] <<  endl;
        return(true);

    }
    else
        return(false);

}




int findMajorPt(int rowwy, int colly, int color)
{
    //int* center = new int[2]; 
    int i = 0;
    // cout << "chk6" << endl;
    // getchar();
   // cout << "salArray 3" << endl;
    int colorInternal;

    if(color==yellowR)
        colorInternal=yellow;
    else
        colorInternal=color;

    for (int i = 0; i < colly; i++) //resetter block array
        for (int j = 0; j < rowwy; j++) 
            blockArray[i][j]=false;


    int Xtally=0;
    int Ytally=0;//kanskje kjappere med float

// cout << "chk1.2" << endl; 
//     getchar();
    //sjekker blå
    bool Done=false;
    int toBeProcessed[SizeOfProcArray][2];
    int toBeProcessedCounter=0;
    int foundCounter=0;
    // cout << "chk4" << endl;
    // getchar();
    i=0;


    while(!Done)
    {
        //get a pt
        int xx, yy;
        xx=colorpixarray[i][color][0];
        yy=colorpixarray[i][color][1];



        toBeProcessedCounter=1;
        toBeProcessed[toBeProcessedCounter-1][0]=xx;
        toBeProcessed[toBeProcessedCounter-1][1]=yy;

    // cout << "chk5" << endl;
    // getchar();

        
        bool investigate=true;
        while(investigate)
        {

            //få en fra array
            if(toBeProcessedCounter < 1)
                break;
            xx=toBeProcessed[toBeProcessedCounter-1][0];

            yy=toBeProcessed[toBeProcessedCounter-1][1];
            toBeProcessedCounter--;
            
            if(xx > colly || yy > rowwy)
            {
                cout << "error: 56 :" << endl;
                getchar();
            }




            foundCounter++;
            Xtally+=xx;
            Ytally+=yy;


            //top
            if ((yy-1) >0 && !blockArray[xx][yy-1])
            {
                mineo1=src.at<Vec3b>(yy-1, xx); // y, x
                int colorFB= getColor(mineo1);
                if (colorFB==colorInternal)
                {
                    blockArray[xx][yy-1]=true;
                    toBeProcessedCounter++;

                    toBeProcessed[toBeProcessedCounter-1][0]=xx;
                    toBeProcessed[toBeProcessedCounter-1][1]=yy-1;
                }
            }

            //left
            if ((xx-1) >0 && !blockArray[xx-1][yy])
            {
                mineo1=src.at<Vec3b>(yy, xx-1); // y, x
                int colorFB= getColor(mineo1);
                if (colorFB==colorInternal)
                {
                    blockArray[xx-1][yy]=true;
                    toBeProcessedCounter++;
                    toBeProcessed[toBeProcessedCounter-1][0]=xx-1;
                    toBeProcessed[toBeProcessedCounter-1][1]=yy;
                }
            }

            //bottom
            if ((yy+1) < rowwy && !blockArray[xx][yy+1])
            {
                mineo1=src.at<Vec3b>(yy+1, xx); // y, x
                int colorFB= getColor(mineo1);
                if (colorFB==colorInternal)
                {
                    blockArray[xx][yy+1]=true;
                    toBeProcessedCounter++;
                    toBeProcessed[toBeProcessedCounter-1][0]=xx;
                    toBeProcessed[toBeProcessedCounter-1][1]=yy+1;
                }
            }


            //right
            if ((xx+1) < colly && !blockArray[xx+1][yy])
            {
                mineo1=src.at<Vec3b>(yy, xx+1); // y, x
                int colorFB= getColor(mineo1);
                if (colorFB==colorInternal)
                {
                    blockArray[xx+1][yy]=true;
                    toBeProcessedCounter++;
                    toBeProcessed[toBeProcessedCounter-1][0]=xx+1;
                    toBeProcessed[toBeProcessedCounter-1][1]=yy;
                }
            }
            
            if(toBeProcessedCounter>MaxToBeProcOneColor)
            {
                cout << "chk3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###" << endl;
                cout << "chk3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###" << endl;
                cout << "chk3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###k3_-_-§§??88/&¤4###" << endl;
                getchar();

            }                

        



        }
        if (foundCounter>MinPixNumber) //hvis vi har nok
        {
            if(foundCounter>MaxPixNumber) //hvis vi har for mye
            {
                cout << "bubu1 " << foundCounter << endl;
                getchar();
            }

            break;

        }


        i++; //neste "seed-pixel"
        if(counters[1]<=i)//tomt for "seed-pixel"
        {
                cout << "bubu3 " << foundCounter << endl;
                return(2);
            
        }

    }

    int xx;//=Xtally/foundCounter;
    int yy;//=Ytally/foundCounter;

    if (foundCounter>MinPixNumber)
    {

        // getchar();
        xx=Xtally/foundCounter;
        yy=Ytally/foundCounter;
        center[0]=xx;
        center[1]=yy;


    }
    else
    {
        cout << "bubu " << foundCounter << endl;

        center[0]=-20;
        center[1]=-20;


    }
        // center[0]=122;
        // center[1]=122;
        // getchar();
        return(0);

  //  return(center);
}

void funkys()
{
    int pt1[2];//blå
    int pt2[2];//gr
    int pt3[2];//rø
    int pt4[2];//v
    int pt5[2];//h
    


    //return;
    int rowwy=src.rows;
    int colly=src.cols;
    int errorFeedb=0;
    int tmpErrVal=0;
    bool fb=findColorPix(rowwy, colly);




    // getchar();



    if(fb)
    {
        resultatSts=1<<11;
        return; 
    }


    

    tmpErrVal=findMajorPt(rowwy, colly, blue);


    if(tmpErrVal>0)
    {
        errorFeedb = tmpErrVal<<1;
    }



    pt1[0]=center[0];
    pt1[1]=center[1];



    tmpErrVal=findMajorPt(rowwy, colly, green);

    if(tmpErrVal>0)
    {
        errorFeedb &= tmpErrVal<<3;
    }


    pt2[0]=center[0];
    pt2[1]=center[1];




    tmpErrVal=findMajorPt(rowwy, colly, red);

    if(tmpErrVal>0)
    {
        errorFeedb &= tmpErrVal<<5;
    }

    if(center[0]<0)
        cout << "error aa -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ haandtere" << endl;
    pt3[0]=center[0];
    pt3[1]=center[1];
    communicator.saveLastPosProc(4);

    tmpErrVal=findMajorPt(rowwy, colly, yellow);

    if(tmpErrVal>0)
    {
        errorFeedb &= tmpErrVal<<7;
    }


    pt4[0]=center[0];
    pt4[1]=center[1];



    tmpErrVal=findMajorPt(rowwy, colly, yellowR);

    if(tmpErrVal>0)
    {
        errorFeedb &= tmpErrVal<<9;
    }


    pt5[0]=center[0];
    pt5[1]=center[1]; //blå grøn rød y yr



    tegnsirkel(pt1[1],pt1[0]);
    tegnsirkel(pt2[1],pt2[0]);
    tegnsirkel(pt3[1],pt3[0]);
    tegnsirkel(pt4[1],pt4[0]);
    tegnsirkel(pt5[1],pt5[0]);

    #if paintImg
        imshow("nnn",src); 
        waitKey(1);
    #endif


    resultat[0]=vinkel(pt1,pt2);
    resultat[1]=vinkel(pt3,pt1);
//    resultat[2]=vinkel(pt4,pt5);
    resultat[2]=pt3[0]-pt4[0];

    resultatSts=errorFeedb;
    return;    
}