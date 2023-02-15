

//#include "stdafx.h"

#define saveImages 0
#include <opencv2/opencv.hpp>
// Include files to use Opencv API.
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
//#include <opencv2/video/video. hpp>
#include "compileChoice.hpp"
// Include files to use the PYLON API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#include <pylon/PylonGUI.h>
#endif
// Namespace for using pylon objects.
using namespace Pylon;
// Namespace for using Opencv objects.
using namespace cv;
// Namespace for using cout.
using namespace std;
// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 10;
#include "main.hpp"
using namespace std::this_thread; // sleep_for, sleep_until
using namespace std::chrono; // nanoseconds, system_clock, seconds
Pylon::PylonAutoInitTerm autoInitTers;
#include "opencv2/imgproc/imgproc.hpp"

CInstantCamera camera(CTlFactory::GetInstance().CreateFirstDevice());

extern InputFromOtherThreads communicator;
void imgCollector(void)
{
    int feedback=0;

    // Print the model name of the camera.
    cout << "using device " << camera.GetDeviceInfo().GetVendorName() << " " << camera.GetDeviceInfo().GetModelName() << endl;

    // Get a camera nodemap in order to access camera parameters.
    GenApi::INodeMap& nodemap= camera.GetNodeMap();

    //¢f Open the camera before accessing any parameters.
    camera.Open();



    //f/f Create pointers to access the camera Width and Height parameters.

    GenApi::CIntegerPtr width= nodemap.GetNode( "width");
    GenApi::CIntegerPtr height= nodemap.GetNode("Height");

    //ff The pacameter MaxtuaBuffer can be used to control the count of buffers
    //ff allocated for grabbing. The default value of this parameter is 16.

    camera.MaxNumBuffer = 5;

    //ff Create a pylon ImageFormatConverter object.
    CImageFormatConverter formatconverter;
    //ff Specify the output pixel format.
    formatconverter.OutputPixelFormat=PixelType_BGR8packed;
    //tf Create a Pylonimage that will be used to create Opentv images later.
    CPylonImage pylonImage;
    //f/ Declare an integer variable to count the number of grabbed images
    //ff and create image file names with ascending number.
    int grabbedImages= 0;



    // Create an OpenCv video creator.
    //f/f Create an Opencv image.

    Mat openCvImage;

    


int IDft=0;

    camera.StartGrabbing(GrabStrategy_LatestImageOnly);
    // This smart pointer will receive the grab result data.

    CGrabResultPtr ptrGrabResult;

    //f Camara.StopGrabbing() is called automatically by the RetrieveResult() method
    // when c_countOfImagesToGrab images have been retrieved.
    int county=0;
    while( camera.IsGrabbing())
    {
        //¢f wait for an image and then retrieve it. A timeout of S00@ ms is used. .
        camera. RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException);
        //df Image grabbed successfully?

        if(ptrGrabResult -> GrabSucceeded())
        {
            IDft++;
            // county++;
            // if(county>60)
            // {
            //     county=0;
            //     cout<<"grabbed ----------------------------------------------------"<<endl;
            // }

            //t/ Convert the grabbed buffer to a pylon image.
            formatconverter.Convert(pylonImage, ptrGrabResult);
            //df Create an Opentv image from a pylon image.
            cv::Mat tmp;
            openCvImage= cv::Mat(ptrGrabResult->GetHeight(), ptrGrabResult->GetWidth(), CV_8UC3, (uint8_t *) pylonImage.GetBuffer());
            // cv::bilateralFilter(tmp, openCvImage, -1, 10, 10);

            if(openCvImage.cols == 720)
                feedback=3;
            else
                feedback=0;


                
            if (smallImg)
                cv::resize(openCvImage,openCvImage,Size(360,240));

            //cv::resize(openCvImage,openCvImage2, cv::Size(), 0.75, 0.75);
            //cv::resize(openCvImage,openCvImage2, cv::Size(), 0.75, 0.75);

            FrameTime inputty;
            inputty.frme=openCvImage;
            inputty.IDs=IDft;

            inputty.CmdSts=feedback;
            inputty.empty=false;

            #if paintImg
                imshow("nn",openCvImage); 
                waitKey(1);
            #endif
            communicator.dataImgCollMainPush(inputty);
        }
        else
        {
            cout << "Error: " << ptrGrabResult->GetErrorCode() << " " << ptrGrabResult->GetErrorDescription() << endl;
        }
    }
    cout << "Press Enter to exit.Press Enter to exit.Press Enter to exit.Press Enter to exit.Press Enter to exit." << endl;
}