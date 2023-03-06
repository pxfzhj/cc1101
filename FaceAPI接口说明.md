# FaceAPI 接口使用说明

## 需要使用到的结构体
### 人脸检测框
```c++
struct MyRECT {
    int x;
    int y;
    int width;
    int height;
};
```

### 人脸和特征
```c++
    float feature[128];
```

## 人脸函数
### ⭐人脸检测和特征提取【通过读取图像文件】
```c++
int FaceDetectAndExtractByFile(const char* imgPath, int size, MyRECT* rects, MyFEAT* feats);
```
#### 函数参数
|  参数   | 描述  |
|  ----  | ----  |
| imgPath(IN)  | 人脸图像文件路径 |
| size(IN)  | 指定存放人脸RECT和FEATURE的大小 |
| rects(OUT)  | 存放人脸RECT的数组首地址 |
| feats(OUT)  | 存放人脸FEATURE的数组首地址 |
#### 返回值
**-1**，检测失败<br>
 **0**，未检测到人脸<br>
检测到人脸，则返回检测到的人脸个数



### ⭐人脸检测和特征提取【通过内存中的图像】
```c++
int FaceDetectAndExtractByBuff(int w, int h, uchar* rgb24, int size, MyRECT* rects, MyFEAT* feats);
```
#### 函数参数
|  参数   | 描述  |
|  ----  | ----  |
| w(IN)  | 图像的宽度 |
| h(IN)  | 图像的高度 |
| rgb24(IN)  | 图像内存地址 |
| size(IN)  | 指定存放人脸RECT和FEATURE的大小 |
| rects(OUT)  | 存放人脸RECT的数组首地址 |
| feats(OUT)  | 存放人脸FEATURE的数组首地址 |
#### 返回值
**-1**，检测失败<br>
 **0**，未检测到人脸<br>
检测到人脸，则返回检测到的人脸个数


### ⭐比较二个特征的相似度
```c++
float FaceCompare(MyFEAT* feat1, MyFEAT* feat2);
```
#### 函数参数
|  参数   | 描述  |
|  ----  | ----  |
| feat1(IN)  | 第一个人脸特征 |
| feat2(IN)  | 第二个人脸特征 |
#### 返回值
***人脸特征的相似度（建议相似度的阀值 >0.95）***
