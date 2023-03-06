#if !defined(__FACE_API_H)
#define __FACE_API_H

#if defined(EXPORT_DLL)
//#define DLL_PUBLIC extern "C" __attribute__((dllexport))
#define DLL_PUBLIC extern "C" __declspec(dllexport)
#else
#define DLL_PUBLIC
typedef unsigned char uchar;
#endif

struct MyRECT {
    int x;
    int y;
    int width;
    int height;
};

struct MyFEAT {
    float feature[128];
};

/*
函数描述：
    通过读取文件来做人脸检测和特征提取

参数描述：
    imgPath(IN): 人脸图像文件路径
    size(IN): 指定存放人脸RECT和FEATURE的大小
    rects(OUT): 存放人脸RECT的数组首地址
    feats(OUT): 存放人脸FEATURE的数组首地址

返回值：
    -1，表示检测失败
    0，表示未检测到人脸
    检测到人脸，则返回人脸的个数
*/
DLL_PUBLIC int FaceDetectAndExtractByFile(const char* imgPath, int size, MyRECT* rects, MyFEAT* feats);


/*
函数描述：
    通过传RGB24的内存来进行人脸检测和特征提取

参数描述：
    w(IN): 图像的宽度
    h(IN): 图像的高度
    rgb24(IN): 图像内存
    size(IN): 指定存放人脸RECT和FEATURE的大小
    rects(OUT): 存放人脸RECT的数组首地址
    feats(OUT): 存放人脸FEATURE的数组首地址

返回值：
    -1，表示检测失败
    0，表示未检测到人脸
    检测到人脸，则返回人脸的个数
*/
DLL_PUBLIC int FaceDetectAndExtractByBuff(int w, int h, uchar* rgb24, int size, MyRECT* rects, MyFEAT* feats);


/*
函数描述：
    比较二个特征的相似度

参数描述：
    feat1[IN]: 第一个人脸特征
    feat2[IN]: 第二个人脸特征

返回值：
    人脸特征的相似度（建议相似度的阀值 >0.95）
*/
DLL_PUBLIC float FaceCompare(MyFEAT* feat1, MyFEAT* feat2);

#endif