// ConsoleApplication1.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。

#include <iostream>
#include <Windows.h>
#include <Shlwapi.h>
#include "FaceAPI.h"

#pragma comment(lib, "shlwapi.lib")

using FT_FaceDetectAndExtractByFile = int(*)(const char*, int, MyRECT*, MyFEAT*);
using FT_FaceCompare = float(*)(MyFEAT*,MyFEAT*);

static const char* GetExePath() {
    static char sExePath[MAX_PATH] = { 0 };
    if (strlen(sExePath)) return sExePath;
    GetModuleFileNameA(NULL, sExePath, sizeof(sExePath));
    PathRemoveFileSpecA(sExePath);
    return strlen(sExePath) ? sExePath : nullptr;
}


int main()
{
    std::cout << "Hello World!\n" << std::endl;

#if 1//动态加载人脸算法(动态加载方便后面升级，在接口不变的情况下，可以直接替换)
    std::string dllPath = std::string(GetExePath()) + std::string("\\FaceAPI.dll");
    HMODULE hModule = LoadLibraryA(dllPath.c_str());
    if (!hModule) {
        std::cout << "Load FaceAPI.dll failed, error code: " << GetLastError() << std::endl;
        return -1;
    }
    FT_FaceDetectAndExtractByFile   FaceDetectAndExtractByFile  = (FT_FaceDetectAndExtractByFile)GetProcAddress(hModule, "FaceDetectAndExtractByFile");
    FT_FaceCompare                  FaceCompare                 = (FT_FaceCompare)GetProcAddress(hModule, "FaceCompare");
#endif

    const char* IMG_PATH = "D:\\github\\dlib-master\\MySamples\\gcc\\test_faces\\古天乐test4.jpg";
    MyRECT rects[16];
    MyFEAT feats[16];
    memset((void*)rects, 0x00, sizeof(rects));
    memset((void*)feats, 0x00, sizeof(feats));
    int num = FaceDetectAndExtractByFile(IMG_PATH, 16, rects, feats);
    std::cout << num << std::endl;
    std::cout << "Line: " << __LINE__ << std::endl;
    std::cout << FaceCompare(&feats[0], &feats[1]) << std::endl;
    std::cout << FaceCompare(&feats[0], &feats[2]) << std::endl;
    std::cout << FaceCompare(&feats[1], &feats[2]) << std::endl;
    std::cin.get();
    return 0;
}


