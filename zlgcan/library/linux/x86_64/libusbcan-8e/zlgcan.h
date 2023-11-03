#ifndef ZLGCAN_H_
#define ZLGCAN_H_
#include <time.h>
#include"canframe.h"
#include "config.h"

//�ӿڿ����Ͷ���
#define ZCAN_PCI5121         1
#define ZCAN_PCI9810         2
#define ZCAN_USBCAN1         3
#define ZCAN_USBCAN2         4
#define ZCAN_USBCAN2A        4
#define ZCAN_PCI9820         5
#define ZCAN_CAN232          6
#define ZCAN_PCI5110         7
#define ZCAN_CANLITE         8
#define ZCAN_ISA9620         9
#define ZCAN_ISA5420         10
#define ZCAN_PC104CAN        11
#define ZCAN_CANETUDP        12
#define ZCAN_CANETE          12
#define ZCAN_DNP9810         13
#define ZCAN_PCI9840         14
#define ZCAN_PC104CAN2       15
#define ZCAN_PCI9820I        16
#define ZCAN_CANETTCP        17
#define ZCAN_PEC9920         18
#define ZCAN_PCIE_9220       18
#define ZCAN_PCI5010U        19
#define ZCAN_USBCAN_E_U      20
#define ZCAN_USBCAN_2E_U     21
#define ZCAN_PCI5020U        22
#define ZCAN_EG20T_CAN       23
#define ZCAN_PCIE9221        24
#define ZCAN_WIFICAN_TCP     25
#define ZCAN_WIFICAN_UDP     26
#define ZCAN_PCIe9120        27
#define ZCAN_PCIe9110        28
#define ZCAN_PCIe9140        29
#define ZCAN_USBCAN_4E_U     31
#define ZCAN_CANDTU          32
#define ZCAN_CANDTU_MINI     33
#define ZCAN_USBCAN_8E_U     34
#define ZCAN_CANREPLAY       35
#define ZCAN_CANDTU_NET      36
#define ZCAN_CANDTU_100UR    37
#define ZCAN_PCIE_CANFD_100U 38
#define ZCAN_PCIE_CANFD_200U 39
#define ZCAN_PCIE_CANFD_400U 40

#define ZCAN_VIRTUAL_DEVICE  99 //�����豸

//CAN������
#define ERR_CAN_OVERFLOW            0x0001 //CAN�������ڲ�FIFO���
#define ERR_CAN_ERRALARM            0x0002 //CAN���������󱨾�
#define	ERR_CAN_PASSIVE             0x0004 //CAN��������������
#define	ERR_CAN_LOSE                0x0008 //CAN�������ٲö�ʧ
#define	ERR_CAN_BUSERR              0x0010 //CAN���������ߴ���
#define ERR_CAN_BUSOFF              0x0020 //���߹رմ���
#define ERR_CAN_BUFFER_OVERFLOW     0x0040 //CAN�������ڲ�BUFFER���
//ͨ�ô�����
#define	ERR_DEVICEOPENED            0x0100 //�豸�Ѿ���
#define	ERR_DEVICEOPEN              0x0200 //���豸����
#define	ERR_DEVICENOTOPEN           0x0400 //�豸û�д�
#define	ERR_BUFFEROVERFLOW          0x0800 //���������
#define	ERR_DEVICENOTEXIST          0x1000 //���豸������
#define	ERR_LOADKERNELDLL           0x2000 //װ�ض�̬��ʧ��
#define ERR_CMDFAILED               0x4000 //ִ������ʧ�ܴ�����
#define	ERR_BUFFERCREATE            0x8000 //�ڴ治��

//CANET������
#define ERR_CANETE_PORTOPENED       0x00010000 //�˿��Ѿ�����
#define ERR_CANETE_INDEXUSED        0x00020000 //�豸�������Ѿ���ռ��
#define ERR_REF_TYPE_ID             0x00030001 //SetReference��GetReference���ݵ�RefType������
#define ERR_CREATE_SOCKET           0x00030002 //����Socketʧ��
#define ERR_OPEN_CONNECT            0x00030003 //��Socket������ʱʧ�ܣ������豸�����Ѿ�����
#define ERR_NO_STARTUP              0x00030004 //�豸û����
#define ERR_NO_CONNECTED            0x00030005 //�豸������
#define ERR_SEND_PARTIAL            0x00030006 //ֻ�����˲��ֵ�CAN֡
#define ERR_SEND_TOO_FAST           0x00030007 //���ݷ���̫�죬Socket����������

//�������÷���״ֵ̬
#define	STATUS_OK                   1
#define STATUS_ERR                  0

#define CMD_DESIP                   0
#define CMD_DESPORT                 1
#define CMD_CHGDESIPANDPORT         2
#define CMD_SRCPORT                 2
#define CMD_TCP_TYPE                4 //tcp ������ʽ��������:1 ���ǿͻ���:0
#define TCP_CLIENT                  0
#define TCP_SERVER                  1
//��������ʽ����Ч
#define CMD_CLIENT_COUNT            5 //�����ϵĿͻ��˼���
#define CMD_CLIENT                  6 //�����ϵĿͻ���
#define CMD_DISCONN_CLINET          7 //�Ͽ�һ������
#define CMD_SET_RECONNECT_TIME      8 //ʹ���Զ�����

#define TYPE_CAN   0
#define TYPE_CANFD 1

typedef unsigned char    BYTE;
//typedef unsigned int     UINT;
typedef unsigned long long UINT64;
typedef int              INT;
//typedef unsigned short   USHORT;
//typedef unsigned char    UCHAR;

typedef void * DEVICE_HANDLE;
typedef void * CHANNEL_HANDLE;

typedef struct tagZCAN_DEVICE_INFO {
    USHORT hw_Version;
    USHORT fw_Version;
    USHORT dr_Version;
    USHORT in_Version;
    USHORT irq_Num;
    BYTE   can_Num;
    UCHAR  str_Serial_Num[20];
    UCHAR  str_hw_Type[40];
    USHORT reserved[4];
}ZCAN_DEVICE_INFO;

typedef struct tagZCAN_CHANNEL_INIT_CONFIG {
    UINT can_type; // 0:can 1:canfd
    union
    {
        struct
        {
            UINT  acc_code; // ������
            UINT  acc_mask; // ������
            UINT  reserved; // ����
            BYTE  filter;   // 0-˫����, 1-������
            BYTE  timing0;  // ��ʱ��0
            BYTE  timing1;  // ��ʱ��1
            BYTE  mode;     // 0-����, 1-ֻ��
        }can;
        struct
        {
            UINT   acc_code; // ������
            UINT   acc_mask; // ������
            UINT   timing0;  // �ٲ���ʱ��
            UINT   timing1;  // ������ʱ��
            UINT   brp;      // ������Ԥ��Ƶ����
            BYTE   filter;   // 0-˫����, 1-������
            BYTE   mode;     // 0-����, 1-ֻ��
            USHORT pad;      // ����
            UINT   reserved; // ����
        }canfd;
    };
}ZCAN_CHANNEL_INIT_CONFIG;

typedef struct tagZCAN_CHANNEL_ERR_INFO {
    UINT error_code;
    BYTE passive_ErrData[3];
    BYTE arLost_ErrData;
} ZCAN_CHANNEL_ERR_INFO;

typedef struct tagZCAN_CHANNEL_STATUS {
    BYTE errInterrupt;
    BYTE regMode;
    BYTE regStatus;
    BYTE regALCapture;
    BYTE regECCapture;
    BYTE regEWLimit;
    BYTE regRECounter;
    BYTE regTECounter;
    UINT Reserved;
}ZCAN_CHANNEL_STATUS;

typedef struct tagZCAN_Transmit_Data
{
    can_frame frame;
    UINT transmit_type;//0:��������, 1:���η���, 2:�Է�����, 3:�����Է�����
}ZCAN_Transmit_Data;

typedef struct tagZCAN_Receive_Data
{
    can_frame frame;
    UINT64    timestamp;       //��λΪ΢��
}ZCAN_Receive_Data;

typedef struct tagZCAN_TransmitFD_Data
{
    canfd_frame frame;
    UINT transmit_type;
}ZCAN_TransmitFD_Data;

typedef struct tagZCAN_ReceiveFD_Data
{
    canfd_frame frame;
    UINT64      timestamp;       //��λΪ΢��
}ZCAN_ReceiveFD_Data;

//CAN��ʱ�Զ�����֡�ṹ
typedef struct tagZCAN_AUTO_TRANSMIT_OBJ{
    USHORT enable;//ʹ�ܱ�������.  0������   1��ʹ��
    USHORT index;  //���ı��, 0...
    UINT   interval;//��ʱ����ʱ�䡣1msΪ��λ
    ZCAN_Transmit_Data obj;//����
}ZCAN_AUTO_TRANSMIT_OBJ, *PZCAN_AUTO_TRANSMIT_OBJ;

//CANFD��ʱ�Զ�����֡�ṹ
typedef struct tagZCANFD_AUTO_TRANSMIT_OBJ{
    UINT interval;//��ʱ����ʱ�䡣1msΪ��λ
    ZCAN_TransmitFD_Data obj;//����
}ZCANFD_AUTO_TRANSMIT_OBJ, *PZCANFD_AUTO_TRANSMIT_OBJ;

#ifdef __cplusplus
extern "C"
{
#endif
//�豸����
#define INVALID_DEVICE_HANDLE 0
DEVICE_HANDLE ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
INT ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
INT ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);

//canͨ������
#define INVALID_CHANNEL_HANDLE 0
CHANNEL_HANDLE ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index, ZCAN_CHANNEL_INIT_CONFIG* pInitConfig);
INT ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
INT ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
INT ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
INT ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
INT ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
INT ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
INT ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);
INT ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, INT wait_time);
INT ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
INT ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, INT wait_time);

IProperty* GetIProperty(DEVICE_HANDLE device_handle);   //��ȡ���Խӿ�
INT ReleaseIProperty(IProperty * pIProperty);

#ifdef __cplusplus
}
#endif

#endif //ZLGCAN_H_
