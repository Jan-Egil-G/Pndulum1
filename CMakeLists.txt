# CMakeList.txt : CMake project for CMakeProject1, include source and define
# project specific logic here.
#

# TODO: Add tests and install targets if needed.

cmake_minimum_required(VERSION 3.0.0)
project("doublepend2")

include(CTest)
enable_testing()
set(OpenCV_DIR "C:/PyPj/cpp/opcvBuild/build6/install/x64/vc16/lib")
set(PYLON_DEV_DIR "C:/Program Files/Basler/pylon 7/Development/include")
set(PYLON_LIB_DIR "C:/Program Files/Basler/pylon 7/Development/lib/x64")

#set(OpenCV_DIR "C:/PyPj/cpp/opcvBuild/build6/install/")
find_package( OpenCV REQUIRED )
#add_library(${OpenCV_LIBS})
include_directories( ${OpenCV_INCLUDE_DIRS} )
include_directories( ${PYLON_DEV_DIR} )

link_directories(${PYLON_LIB_DIR})
message(STATUS "message to display:   ${OpenCV_LIBS}")

set(SOURCES main.cpp main.hpp imageCollection.hpp imageCollection.cpp communicat.hpp communicat.cpp imageProcessing.hpp imageProcessing.cpp FileWriter.hpp FileWriter.cpp)

add_executable(doublepend2 ${SOURCES})


#include_directories(${CMAKE_SOURCE_DIR}/inc)
#link_directories(${OpenCV_DIR})



target_include_directories(doublepend2 PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}")



target_link_libraries(doublepend2 ${OpenCV_LIBS} )
target_link_libraries(doublepend2 GCBase_MD_VC141_v3_1_Basler_pylon;GenApi_MD_VC141_v3_1_Basler_pylon;PylonBase_v7_2;PylonC;PylonDataProcessing_v1_1;PylonGUI_v7_2;PylonUtility_v7_2)


set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
