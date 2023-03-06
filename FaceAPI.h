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
����������
    ͨ����ȡ�ļ�������������������ȡ

����������
    imgPath(IN): ����ͼ���ļ�·��
    size(IN): ָ���������RECT��FEATURE�Ĵ�С
    rects(OUT): �������RECT�������׵�ַ
    feats(OUT): �������FEATURE�������׵�ַ

����ֵ��
    -1����ʾ���ʧ��
    0����ʾδ��⵽����
    ��⵽�������򷵻������ĸ���
*/
DLL_PUBLIC int FaceDetectAndExtractByFile(const char* imgPath, int size, MyRECT* rects, MyFEAT* feats);


/*
����������
    ͨ����RGB24���ڴ���������������������ȡ

����������
    w(IN): ͼ��Ŀ��
    h(IN): ͼ��ĸ߶�
    rgb24(IN): ͼ���ڴ�
    size(IN): ָ���������RECT��FEATURE�Ĵ�С
    rects(OUT): �������RECT�������׵�ַ
    feats(OUT): �������FEATURE�������׵�ַ

����ֵ��
    -1����ʾ���ʧ��
    0����ʾδ��⵽����
    ��⵽�������򷵻������ĸ���
*/
DLL_PUBLIC int FaceDetectAndExtractByBuff(int w, int h, uchar* rgb24, int size, MyRECT* rects, MyFEAT* feats);


/*
����������
    �Ƚ϶������������ƶ�

����������
    feat1[IN]: ��һ����������
    feat2[IN]: �ڶ�����������

����ֵ��
    �������������ƶȣ��������ƶȵķ�ֵ >0.95��
*/
DLL_PUBLIC float FaceCompare(MyFEAT* feat1, MyFEAT* feat2);

#endif