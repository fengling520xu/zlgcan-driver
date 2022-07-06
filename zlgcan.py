"""
by zhuyu4839@gmail.com
"""
import inspect
import logging
import os
import platform
import re
import warnings
from ctypes import *

_curr_path = os.path.split(os.path.realpath(__file__))[0]
_arch, _os = platform.architecture()
_is_windows, _is_linux = False, False
if 'windows' in _os.lower():
    _is_windows = True
    if _arch == '32bit':
        _lib_path = os.path.join(_curr_path, 'windows/x86/zlgcan/zlgcan.dll')
    else:
        _lib_path = os.path.join(_curr_path, 'windows/x86_64/zlgcan/zlgcan.dll')
    _library = windll.LoadLibrary(_lib_path)
elif 'linux' in _os.lower():
    _is_linux = True
    if _arch == '64bit':
        _lib_path = os.path.join(_curr_path, 'linux/x86_64/zlgcan/libusbcanfd.so')
    else:
        _lib_path = None
    _library = cdll.LoadLibrary(_lib_path)
else:
    _library = None


class ZCANException(Exception):
    pass


class ZCANMessageType:
    LIN = c_uint(-1)
    CAN = c_uint(0)
    CANFD = c_uint(1)


class ZCANCanFdStd:
    ISO = 0
    NON_ISO = 0


class ZCANProtocol:
    CAN = 0
    CANFD_ISO = 1
    CANFD_NON_ISO = 2


class ZCANCanMode:
    NORMAL = 0
    READ_ONLY = 1
    # PCIECANFD-100U、PCIECANFD-400U、MiniPCIeCANFD、M.2CANFD支持
    SELF_SR = 2             # 自发自收
    SINGLE_SEND = 3         # 单次发送模式, 送失败时不会进行重发, 此时发送超时无效


class ZCANCanTransType:
    NORMAL = 0              # 正常发送
    SINGLE = 1              # 单次发送
    SELF_SR = 2             # 自发自收
    SINGLE_SELF_SR = 3      # 单次自发自收


class ZCANCanFilter:
    SINGLE = 1
    DOUBLE = 0


class ZCANCanType:
    CAN = c_uint(0)
    CANFD = c_uint(1)


ZCAN_DEVICE_TYPE = c_uint


class ZCANDeviceType:
    ZCAN_PCI5121                       = ZCAN_DEVICE_TYPE(1)
    ZCAN_PCI9810                       = ZCAN_DEVICE_TYPE(2)
    ZCAN_USBCAN1                       = ZCAN_DEVICE_TYPE(3)
    ZCAN_USBCAN2                       = ZCAN_DEVICE_TYPE(4)
    ZCAN_PCI9820                       = ZCAN_DEVICE_TYPE(5)
    ZCAN_CAN232                        = ZCAN_DEVICE_TYPE(6)
    ZCAN_PCI5110                       = ZCAN_DEVICE_TYPE(7)
    ZCAN_CANLITE                       = ZCAN_DEVICE_TYPE(8)
    ZCAN_ISA9620                       = ZCAN_DEVICE_TYPE(9)
    ZCAN_ISA5420                       = ZCAN_DEVICE_TYPE(10)
    ZCAN_PC104CAN                      = ZCAN_DEVICE_TYPE(11)
    ZCAN_CANETUDP                      = ZCAN_DEVICE_TYPE(12)
    ZCAN_CANETE                        = ZCAN_DEVICE_TYPE(12)
    ZCAN_DNP9810                       = ZCAN_DEVICE_TYPE(13)
    ZCAN_PCI9840                       = ZCAN_DEVICE_TYPE(14)
    ZCAN_PC104CAN2                     = ZCAN_DEVICE_TYPE(15)
    ZCAN_PCI9820I                      = ZCAN_DEVICE_TYPE(16)
    ZCAN_CANETTCP                      = ZCAN_DEVICE_TYPE(17)
    ZCAN_PCIE_9220                     = ZCAN_DEVICE_TYPE(18)
    ZCAN_PCI5010U                      = ZCAN_DEVICE_TYPE(19)
    ZCAN_USBCAN_E_U                    = ZCAN_DEVICE_TYPE(20)
    ZCAN_USBCAN_2E_U                   = ZCAN_DEVICE_TYPE(21)
    ZCAN_PCI5020U                      = ZCAN_DEVICE_TYPE(22)
    ZCAN_EG20T_CAN                     = ZCAN_DEVICE_TYPE(23)
    ZCAN_PCIE9221                      = ZCAN_DEVICE_TYPE(24)
    ZCAN_WIFICAN_TCP                   = ZCAN_DEVICE_TYPE(25)
    ZCAN_WIFICAN_UDP                   = ZCAN_DEVICE_TYPE(26)
    ZCAN_PCIe9120                      = ZCAN_DEVICE_TYPE(27)
    ZCAN_PCIe9110                      = ZCAN_DEVICE_TYPE(28)
    ZCAN_PCIe9140                      = ZCAN_DEVICE_TYPE(29)
    ZCAN_USBCAN_4E_U                   = ZCAN_DEVICE_TYPE(31)
    ZCAN_CANDTU_200UR                  = ZCAN_DEVICE_TYPE(32)
    ZCAN_CANDTU_MINI                   = ZCAN_DEVICE_TYPE(33)
    ZCAN_USBCAN_8E_U                   = ZCAN_DEVICE_TYPE(34)
    ZCAN_CANREPLAY                     = ZCAN_DEVICE_TYPE(35)
    ZCAN_CANDTU_NET                    = ZCAN_DEVICE_TYPE(36)
    ZCAN_CANDTU_100UR                  = ZCAN_DEVICE_TYPE(37)
    ZCAN_PCIE_CANFD_100U               = ZCAN_DEVICE_TYPE(38)
    ZCAN_PCIE_CANFD_200U               = ZCAN_DEVICE_TYPE(39)
    ZCAN_PCIE_CANFD_400U               = ZCAN_DEVICE_TYPE(40)
    ZCAN_USBCANFD_200U                 = ZCAN_DEVICE_TYPE(41)
    ZCAN_USBCANFD_100U                 = ZCAN_DEVICE_TYPE(42)
    ZCAN_USBCANFD_MINI                 = ZCAN_DEVICE_TYPE(43)
    ZCAN_CANFDCOM_100IE                = ZCAN_DEVICE_TYPE(44)
    ZCAN_CANSCOPE                      = ZCAN_DEVICE_TYPE(45)
    ZCAN_CLOUD                         = ZCAN_DEVICE_TYPE(46)
    ZCAN_CANDTU_NET_400                = ZCAN_DEVICE_TYPE(47)
    ZCAN_CANFDNET_TCP                  = ZCAN_DEVICE_TYPE(48)
    ZCAN_CANFDNET_200U_TCP             = ZCAN_DEVICE_TYPE(48)
    ZCAN_CANFDNET_UDP                  = ZCAN_DEVICE_TYPE(49)
    ZCAN_CANFDNET_200U_UDP             = ZCAN_DEVICE_TYPE(49)
    ZCAN_CANFDWIFI_TCP                 = ZCAN_DEVICE_TYPE(50)
    ZCAN_CANFDWIFI_100U_TCP            = ZCAN_DEVICE_TYPE(50)
    ZCAN_CANFDWIFI_UDP                 = ZCAN_DEVICE_TYPE(51)
    ZCAN_CANFDWIFI_100U_UDP            = ZCAN_DEVICE_TYPE(51)
    ZCAN_CANFDNET_400U_TCP             = ZCAN_DEVICE_TYPE(52)
    ZCAN_CANFDNET_400U_UDP             = ZCAN_DEVICE_TYPE(53)
    ZCAN_CANFDBLUE_200U                = ZCAN_DEVICE_TYPE(54)
    ZCAN_CANFDNET_100U_TCP             = ZCAN_DEVICE_TYPE(55)
    ZCAN_CANFDNET_100U_UDP             = ZCAN_DEVICE_TYPE(56)
    ZCAN_CANFDNET_800U_TCP             = ZCAN_DEVICE_TYPE(57)
    ZCAN_CANFDNET_800U_UDP             = ZCAN_DEVICE_TYPE(58)
    ZCAN_USBCANFD_800U                 = ZCAN_DEVICE_TYPE(59)
    ZCAN_PCIE_CANFD_100U_EX            = ZCAN_DEVICE_TYPE(60)
    ZCAN_PCIE_CANFD_400U_EX            = ZCAN_DEVICE_TYPE(61)
    ZCAN_PCIE_CANFD_200U_MINI          = ZCAN_DEVICE_TYPE(62)
    ZCAN_PCIE_CANFD_200U_M2            = ZCAN_DEVICE_TYPE(63)
    ZCAN_CANFDDTU_400_TCP              = ZCAN_DEVICE_TYPE(64)
    ZCAN_CANFDDTU_400_UDP              = ZCAN_DEVICE_TYPE(65)
    ZCAN_CANFDWIFI_200U_TCP            = ZCAN_DEVICE_TYPE(66)
    ZCAN_CANFDWIFI_200U_UDP            = ZCAN_DEVICE_TYPE(67)

    ZCAN_OFFLINE_DEVICE                = ZCAN_DEVICE_TYPE(98)
    ZCAN_VIRTUAL_DEVICE                = ZCAN_DEVICE_TYPE(99)


ZUSBCANFD_TYPE = (ZCANDeviceType.ZCAN_USBCANFD_200U,
                  ZCANDeviceType.ZCAN_USBCANFD_100U,
                  ZCANDeviceType.ZCAN_USBCANFD_MINI)
ZUSBCAN_XE_U_TYPE = (ZCANDeviceType.ZCAN_USBCAN_E_U,
                     ZCANDeviceType.ZCAN_USBCAN_2E_U,
                     ZCANDeviceType.ZCAN_USBCAN_4E_U)
ZUSBCAN_I_II_TYPE = (ZCANDeviceType.ZCAN_USBCAN1,
                     ZCANDeviceType.ZCAN_USBCAN2)
ZCAN_MERGE_SUPPORT_TYPE = (ZCANDeviceType.ZCAN_USBCANFD_200U,
                           ZCANDeviceType.ZCAN_USBCANFD_100U,
                           ZCANDeviceType.ZCAN_USBCANFD_MINI,
                           ZCANDeviceType.ZCAN_USBCANFD_800U,
                           )

INVALID_DEVICE_HANDLE = 0
INVALID_CHANNEL_HANDLE = 0

ZCAN_ERROR_CAN_OVERFLOW            = 0x0001
ZCAN_ERROR_CAN_ERRALARM            = 0x0002
ZCAN_ERROR_CAN_PASSIVE             = 0x0004
ZCAN_ERROR_CAN_LOSE                = 0x0008
ZCAN_ERROR_CAN_BUSERR              = 0x0010
ZCAN_ERROR_CAN_BUSOFF              = 0x0020
ZCAN_ERROR_CAN_BUFFER_OVERFLOW     = 0x0040

ZCAN_ERROR_DEVICEOPENED            = 0x0100
ZCAN_ERROR_DEVICEOPEN              = 0x0200
ZCAN_ERROR_DEVICENOTOPEN           = 0x0400
ZCAN_ERROR_BUFFEROVERFLOW          = 0x0800
ZCAN_ERROR_DEVICENOTEXIST          = 0x1000
ZCAN_ERROR_LOADKERNELDLL           = 0x2000
ZCAN_ERROR_CMDFAILED               = 0x4000
ZCAN_ERROR_BUFFERCREATE            = 0x8000

ZCAN_ERROR_CANETE_PORTOPENED       = 0x00010000
ZCAN_ERROR_CANETE_INDEXUSED        = 0x00020000
ZCAN_ERROR_REF_TYPE_ID             = 0x00030001
ZCAN_ERROR_CREATE_SOCKET           = 0x00030002
ZCAN_ERROR_OPEN_CONNECT            = 0x00030003
ZCAN_ERROR_NO_STARTUP              = 0x00030004
ZCAN_ERROR_NO_CONNECTED            = 0x00030005
ZCAN_ERROR_SEND_PARTIAL            = 0x00030006
ZCAN_ERROR_SEND_TOO_FAST           = 0x00030007

ZCAN_STATUS_ERR                    = 0
ZCAN_STATUS_OK                     = 1
ZCAN_STATUS_ONLINE                 = 2
ZCAN_STATUS_OFFLINE                = 3
ZCAN_STATUS_UNSUPPORTED            = 4

ZCAN_CMD_DESIP                     = 0
ZCAN_CMD_DESPORT                   = 1
ZCAN_CMD_CHGDESIPANDPORT           = 2
ZCAN_CMD_SRCPORT                   = 2
ZCAN_CMD_TCP_TYPE                  = 4
ZCAN_TCP_CLIENT                    = 0
ZCAN_TCP_SERVER                    = 1

ZCAN_CMD_CLIENT_COUNT              = 5
ZCAN_CMD_CLIENT                    = 6
ZCAN_CMD_DISCONN_CLINET            = 7
ZCAN_CMD_SET_RECONNECT_TIME        = 8

ZCAN_TYPE_CAN                      = 0
ZCAN_TYPE_CANFD                    = 1
ZCAN_TYPE_ALL_DATA                 = 2

ZCLOUD_MAX_DEVICES                 = 100
ZCLOUD_MAX_CHANNEL                 = 16

ZCAN_LIN_MODE_MASTER               = 0
ZCAN_LIN_MODE_SLAVE                = 1
ZCAN_LIN_FLAG_CHK_ENHANCE          = 0x01
ZCAN_LIN_FLAG_VAR_DLC              = 0x02


_path = lambda ch, path: f'{ch}/{path}' if ch else f'{path}'
_version = lambda version: ("V%02x.%02x" if version // 0xFF >= 9 else "V%d.%02x") % (version // 0xFF, version & 0xFF)


class ZCAN_DEVICE_INFO(Structure):  # ZCAN_DEVICE_INFO
    """
    Device information
    """
    _fields_ = [("hw_Version", c_ushort),
                ("fw_Version", c_ushort),
                ("dr_Version", c_ushort),
                ("in_Version", c_ushort),
                ("irq_Num", c_ushort),
                ("can_Num", c_ubyte),
                ("str_Serial_Num", c_ubyte * 20),
                ("str_hw_Type", c_ubyte * 40),
                ("reserved", c_ushort * 4)]

    def __str__(self):
        return f"Hardware Version : {self.hw_version}\n" \
               f"Firmware Version : {self.fw_version}\n" \
               f"Driver Version   : {self.dr_version}\n" \
               f"Interface Version: {self.in_version}\n" \
               f"Interrupt Number : {self.irq_num}\n" \
               f"CAN Number       : {self.can_num}\n" \
               f"Serial           : {self.serial}\n" \
               f"Hardware Type    : {self.hw_type}"

    @property
    def hw_version(self):
        return _version(self.hw_Version)

    @property
    def fw_version(self):
        return _version(self.fw_Version)

    @property
    def dr_version(self):
        return _version(self.dr_Version)

    @property
    def in_version(self):
        return _version(self.in_Version)

    @property
    def irq_num(self):
        return self.irq_Num

    @property
    def can_num(self):
        return self.can_Num

    @property
    def serial(self):
        return bytes(self.str_Serial_Num).decode('utf-8')

    @property
    def hw_type(self):
        return bytes(self.str_hw_Type).decode('utf-8')


class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):     # _ZCAN_CHANNEL_CAN_INIT_CONFIG
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("reserved", c_uint),
                ("filter", c_ubyte),
                ("timing0", c_ubyte),
                ("timing1", c_ubyte),
                ("mode", c_ubyte)]

class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):    # _ZCAN_CHANNEL_CANFD_INIT_CONFIG
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("abit_timing", c_uint),
                ("dbit_timing", c_uint),
                ("brp", c_uint),
                ("filter", c_ubyte),
                ("mode", c_ubyte),
                ("pad", c_ushort),
                ("reserved", c_uint)]

class _ZCAN_CHANNEL_INIT_CONFIG(Union):         # union in ZCAN_CHANNEL_INIT_CONFIG
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]

class ZCAN_CHANNEL_INIT_CONFIG(Structure):       # ZCAN_CHANNEL_INIT_CONFIG
    _fields_ = [("can_type", c_uint),
                ("config", _ZCAN_CHANNEL_INIT_CONFIG)]

class ZCAN_CHANNEL_ERR_INFO(Structure):           # ZCAN_CHANNEL_ERR_INFO
    ERROR_CODE = {
        0x0001: 'CAN FIFO Overflow',
        0x0002: 'CAN Error Warning',
        0x0004: 'CAN Passive Error',
        0x0008: 'CAN Arbitration Lost',
        0x0010: 'CAN Bus Error',
        0x0020: 'CAN Bus closed',
        0x0040: 'CAN Cache Overflow'
    }
    _fields_ = [("error_code", c_uint),
                ("passive_ErrData", c_ubyte * 3),
                ("arLost_ErrData", c_ubyte)]

    def __str__(self):
        return f'error info           : {self.ERROR_CODE[self.error_code]} \n' \
               f'passive error info   : {bytes(self.passive_ErrData).hex()} \n' \
               f'arbitration lost info: {self.arLost_ErrData}'

class ZCAN_CHANNEL_STATUS(Structure):         # ZCAN_CHANNEL_STATUS
    _fields_ = [("errInterrupt", c_ubyte),
                ("regMode", c_ubyte),
                ("regStatus", c_ubyte),
                ("regALCapture", c_ubyte),
                ("regECCapture", c_ubyte),
                ("regEWLimit", c_ubyte),
                ("regRECounter", c_ubyte),
                ("regTECounter", c_ubyte),
                ("Reserved", c_ubyte)]

class ZCAN_CAN_FRAME(Structure):               # ZCAN_CAN_FRAME
    _fields_ = [("can_id", c_uint, 29),
                ("err", c_uint, 1),         # 错误帧标识CANID bit29
                ("rtr", c_uint, 1),         # 远程帧标识CANID bit30
                ("eff", c_uint, 1),         # 扩展帧标识CANID bit31
                ("can_dlc", c_ubyte),       # 数据长度
                ("__pad", c_ubyte),         # 队列模式下bit7为延迟发送标志位
                ("__res0", c_ubyte),        # 队列模式下帧间隔低8位, 单位 ms
                ("__res1", c_ubyte),        # 队列模式下帧间隔高8位, 单位 ms
                ("data", c_ubyte * 8)]

class ZCAN_CANFD_FRAME(Structure):             # ZCAN_CANFD_FRAME
    _fields_ = [("can_id", c_uint, 29),
                ("err", c_uint, 1),         # 错误帧标识CANID bit29
                ("rtr", c_uint, 1),         # 远程帧标识CANID bit30
                ("eff", c_uint, 1),         # 扩展帧标识CANID bit31
                ("len", c_ubyte),           # 数据长度
                ("brs", c_ubyte, 1),        # Bit Rate Switch, flags bit0
                ("esi", c_ubyte, 1),        # Error State Indicator, flags bit1
                ("__res", c_ubyte, 6),      # 保留, flags bit2-7
                ("__res0", c_ubyte),        # 队列模式下帧间隔低8位, 单位 ms
                ("__res1", c_ubyte),        # 队列模式下帧间隔高8位, 单位 ms
                ("data", c_ubyte * 64)]

class ZCAN_Transmit_Data(Structure):            # ZCAN_Transmit_Data
    _pack_ = 1
    _fields_ = [("frame", ZCAN_CAN_FRAME),
                ("transmit_type", c_uint)]      # 0=正常发送, 1=单次发送, 2=自发自收, 3=单次自发自收

class ZCAN_Receive_Data(Structure):             # ZCAN_Receive_Data
    _fields_ = [("frame", ZCAN_CAN_FRAME), ("timestamp", c_ulonglong)]

class ZCAN_TransmitFD_Data(Structure):          # ZCAN_TransmitFD_Data
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]

class ZCAN_ReceiveFD_Data(Structure):           # ZCAN_ReceiveFD_Data
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulonglong)]

class ZCAN_AUTO_TRANSMIT_OBJ(Structure):         # ZCAN_AUTO_TRANSMIT_OBJ
    _fields_ = [("enable", c_ushort),
                ("index", c_ushort),
                ("interval", c_uint),  # ms
                ("obj", ZCAN_Transmit_Data)]

class ZCANFD_AUTO_TRANSMIT_OBJ(Structure):       # ZCANFD_AUTO_TRANSMIT_OBJ
    _fields_ = [("enable", c_ushort),
                ("index", c_ushort),
                ("interval", c_uint),
                ("obj", ZCAN_TransmitFD_Data)]

class ZCANFD_AUTO_TRANSMIT_OBJ_PARAM(Structure):    # ZCANFD_AUTO_TRANSMIT_OBJ_PARAM
    _fields_ = [("index", c_ushort),
                ("type", c_ushort),
                ("value", c_uint)]

class ZCLOUD_CHNINFO(Structure):                       # ZCLOUD_CHNINFO
    _fields_ = [("enable", c_ubyte),                    # // 0:CAN, 1:ISO CANFD, 2:Non-ISO CANFD
                ("type", c_ubyte),
                ("isUpload", c_ubyte),
                ("isDownload", c_ubyte)]

    def __str__(self):
        return f'enable    : {self.enable}\n' \
               f'type      : {self.type}\n' \
               f'isUpload  : {self.isUpload}\n' \
               f'isDownload: {self.isDownload}\n'

class ZCLOUD_DEVINFO(Structure):                        # ZCLOUD_DEVINFO
    _fields_ = [("devIndex", c_int),
                ("type", c_char * 64),
                ("id", c_char * 64),
                ("name", c_char * 64),
                ("owner", c_char * 64),
                ("model", c_char * 64),
                ("fwVer", c_char * 16),
                ("hwVer", c_char * 16),
                ("serial", c_char * 64),
                ("status", c_int),  # 0:online, 1:offline
                ("bGpsUpload", c_ubyte),
                ("channelCnt", c_ubyte),
                ("channels", ZCLOUD_CHNINFO * ZCLOUD_MAX_CHANNEL)]

class ZCLOUD_USER_DATA(Structure):                          # ZCLOUD_USER_DATA
    _fields_ = [("username", c_char * 64),
                ("mobile", c_char * 64),
                ("dllVer", c_char * 16),
                ("devCnt", c_size_t),
                ("channels", ZCLOUD_DEVINFO * ZCLOUD_MAX_DEVICES)]

class _ZCLOUD_GPS_FRAMETime(Structure):
    _fields_ = [("year", c_ushort),
                ("mon", c_ushort),
                ("day", c_ushort),
                ("hour", c_ushort),
                ("min", c_ushort),
                ("sec", c_ushort)]

class ZCLOUD_GPS_FRAME(Structure):                          # ZCLOUD_GPS_FRAME
    _fields_ = [("latitude", c_float),  # + north latitude, - south latitude
                ("longitude", c_float),  # + east longitude, - west longitude
                ("speed", c_float),  # km/h
                ("tm", _ZCLOUD_GPS_FRAMETime)]

class USBCANFDTxTimeStamp(Structure):                    # USBCANFDTxTimeStamp
    _fields_ = [("pTxTimeStampBuffer", POINTER(c_uint)),    # allocated by user, size:nBufferTimeStampCount * 4,unit:100us
                ("nBufferTimeStampCount", c_uint)]          # buffer size

class TxTimeStamp(Structure):                            # TxTimeStamp
    _fields_ = [("pTxTimeStampBuffer", POINTER(c_uint64)),  # allocated by user, size:nBufferTimeStampCount * 8,unit:1us
                ("nBufferTimeStampCount", c_uint),          # buffer timestamp count
                ("nWaitTime", c_int)]                       # Wait Time ms, -1表示等到有数据才返回

class BusUsage(Structure):                               # BusUsage
    _fields_ = [('nTimeStampBegin', c_int64),               # 测量起始时间戳，单位us
                ('nTimeStampEnd', c_int64),                 # 测量结束时间戳，单位us
                ('nChnl', c_ubyte),                         # 通道
                ('nReserved', c_ubyte),                     # 保留
                ('nBusUsage', c_ushort),                    # 总线利用率(%),总线利用率*100展示。取值0~10000，如8050表示80.50%
                ('nFrameCount', c_uint)]                    # 帧数量

class ZCAN_LIN_MSG(Structure):                               # ZCAN_LIN_MSG
    _fields_ = [("ID", c_ubyte),
                ("DataLen", c_byte),
                ("Flag", c_ushort),
                ("TimeStamp", c_uint),
                ("Data", c_ubyte * 8)]

class ZCAN_LIN_INIT_CONFIG(Structure):                   # ZCAN_LIN_INIT_CONFIG
    _fields_ = [("linMode", c_ubyte),
                ("linFlag", c_byte),
                ("reserved", c_ushort),
                ("linBaud", c_uint)]

class _ZCANCANFDDataFlag(Structure):              # ZCANdataFlag
    # _fields_ = [("unionVal", _ZlgCanFdDataFlagVal), ("rawVal", c_uint)]
    _pack_ = 1
    _fields_ = [("frameType", c_uint, 2),       # 0-can,1-canfd
                ("txDelay", c_uint, 2),         # 队列发送延时，延时时间存放在 timeStamp 字段
                                                # 0：不启用延时,
                                                # 1：启用延时，延时时间单位为 1 毫秒(1ms),
                                                # 2：启用延时，延时时间单位为 100 微秒(0.1ms)
                ("transmitType", c_uint, 4),    # 发送方式，0-正常发送, 1：单次发送, 2：自发自收, 3：单次自发自收
                ("txEchoRequest", c_uint, 1),   # 发送回显请求，0-不回显，1-回显
                ("txEchoed", c_uint, 1),        # 报文是否是发送回显报文, 0：正常总线接收到的报文, 1：本设备发送回显报文
                ("reserved", c_uint, 22)]       # 保留

class ZCANCANFDData(Structure):                  # ZCANCANFDData
    _pack_ = 1
    _fields_ = [("timeStamp", c_uint64),
                ("flag", _ZCANCANFDDataFlag),
                ("extraData", c_ubyte * 4),  # 保留
                ("frame", ZCAN_CANFD_FRAME)]

class ZCANErrorData(Structure):                              # ZCANErrorData
    _pack_ = 1
    _fields_ = [("timeStamp", c_uint64),
                ("errType", c_ubyte),
                ("errSubType", c_ubyte),
                ("nodeState", c_ubyte),
                ("rxErrCount", c_ubyte),
                ("txErrCount", c_ubyte),
                ("errData", c_ubyte),
                ("reserved", c_ubyte * 2)]

class _ZCANGPSDataTime(Structure):
    _pack_ = 1
    _fields_ = [("year", c_ushort),
                ("mon", c_ushort),
                ("day", c_ushort),
                ("hour", c_ushort),
                ("min", c_ushort),
                ("sec", c_ushort),
                ("milsec", c_ushort)]

class _ZCANGPSDataFlag(Structure):
    # _fields_ = [("unionVal", _ZlgGpsDataFlagVal), ("rawVal", c_ushort)]
    _pack_ = 1
    _fields_ = [("timeValid", c_ushort, 1),         # 时间数据是否有效
                ("latlongValid", c_ushort, 1),      # 经纬度数据是否有效
                ("altitudeValid", c_ushort, 1),     # 海拔数据是否有效
                ("speedValid", c_ushort, 1),        # 速度数据是否有效
                ("courseAngleValid", c_ushort, 1),  # 航向角数据是否有效
                ("reserved", c_ushort, 13)]         # 保留

class ZCANGPSData(Structure):                        # ZCANGPSData
    _pack_ = 1
    _fields_ = [("time", _ZCANGPSDataTime),
                ("flag", _ZCANGPSDataFlag),
                ("latitude", c_float),              # 纬度 正数表示北纬, 负数表示南纬
                ("longitude", c_float),             # 经度 正数表示东经, 负数表示西经
                ("altitude", c_float),              # 海拔 单位: 米
                ("speed", c_float),                 # 速度 单位: km/h
                ("courseAngle", c_float)]           # 航向角

class _ZCANLINDataPid(Structure):
    # _fields_ = [("unionVal", _ZlgLinDataPidVal), ("rawVal", c_ubyte)]
    _pack_ = 1
    _fields_ = [('ID', c_ubyte, 6),
                ('Parity', c_ubyte, 2)]

class _ZCANLINDataFlag(Structure):
    _pack_ = 1
    # _fields_ = [("unionVal", _ZlgLinDataFlagVal), ("rawVal", c_ushort)]
    _fields_ = [('tx', c_ushort, 1),                # 控制器发送在总线上的消息, 接收有效
                ('rx', c_ushort, 1),                # 控制器接收总线上的消息, 接收有效
                ('noData', c_ushort, 1),            # 无数据区
                ('chkSumErr', c_ushort, 1),         # 校验和错误
                ('parityErr', c_ushort, 1),         # 奇偶校验错误, 此时消息中的 chksum 无效
                ('syncErr', c_ushort, 1),           # 同步段错误
                ('bitErr', c_ushort, 1),            # 发送时位错误
                ('wakeUp', c_ushort, 1),            # 收到唤醒帧, 此时消息ID|数据长度|数据域|校验值无效
                ('reserved', c_ushort, 8)]          # 保留

class ZCANLINData(Structure):                        # ZCANLINData
    _pack_ = 1
    _fields_ = [("timeStamp", c_uint64),
                ("PID", _ZCANLINDataPid),
                ("dataLen", c_ubyte),               # 数据长度
                ("flag", _ZCANLINDataFlag),
                ("chkSum", c_ubyte),
                ("reserved", c_ubyte * 3),
                ("data", c_ubyte * 8)]

class _ZCANDataObjFlag(Union):
    # _fields_ = [("unionVal", _ZlgDataObjFlagVal), ("rawVal", c_ushort)]
    _pack_ = 1
    _fields_ = [("reserved", c_ushort, 16)]

class _ZCANDataObjData(Union):
    _pack_ = 1
    _fields_ = [("zcanCANFDData", ZCANCANFDData), ("zcanErrData", ZCANErrorData),
                ("zcanGPSData", ZCANGPSData), ("zcanLINData", ZCANLINData), ("raw", c_ubyte * 92)]

# 合并接收数据数据结构, 支持CAN/CANFD/LIN/GPS/错误等不同类型数据
class ZCANDataObj(Structure):                    # ZCANDataObj
    _pack_ = 1
    _fields_ = [("dataType", c_ubyte),          # 数据类型, 参考eZCANDataDEF中 数据类型 部分定义
                                                # 1 - CAN/CANFD 数据，data.zcanCANFDData 有效
                                                # 2 - 错误数据，data.zcanErrData 有效
                                                # 3 - GPS 数据，data.zcanGPSData 有效
                                                # 4 - LIN 数据，data.zcanLINData 有效
                ("chnl", c_ubyte),  # 数据通道
                ("flag", _ZCANDataObjFlag),     # 标志信息, 暂未使用
                ("extraData", c_ubyte * 4),     # 额外数据, 暂未使用
                ("data", _ZCANDataObjData)]     # 实际数据, 联合体，有效成员根据 dataType 字段而定

assert sizeof(ZCANDataObj) == 100
# class ZlgCanDataObj(Structure):                     # from zlgcan echo demo
#     _pack_ = 1
#     _fields_ = [("dataType", c_ubyte),              # can/canfd frame
#                 ("chnl", c_ubyte),                  # can_channel
#                 ("flag", c_ushort),                 # 标志信息, 暂未使用
#                 ("extraData", c_ubyte * 4),         # 标志信息, 暂未使用
#                 ("zcanfddata", ZlgCanFdData),       # 88个字节
#                 ("reserved", c_ubyte * 4)]

class IProperty(Structure):  # IProperty
    _fields_ = [("SetValue", c_void_p),
                ("GetValue", c_void_p),
                ("GetPropertys", c_void_p)]

class ZCAN(object):

    def __init__(self):
        if _library is None:
            raise ZCANException(
                "The ZLG-CAN driver could not be loaded. "
                "Check that you are using 32-bit/64bit Python on Windows or 64bit Python on Linux."
            )
        self._logger = logging.getLogger(self.__class__.__name__)
        self._dev_handler = None
        self._dev_index = None
        self._dev_type = None
        # self._dev_type_name = None
        self._dev_info = None
        self._dev_is_canfd = None
        self._channels = ()
        # {'CAN': {chl_obj: is_canfd}, 'LIN': {chl_obj: is_master}}
        self._channel_handlers = {'CAN': [], 'LIN': []}

    @property
    def device_index(self):
        return self._dev_index

    # @property
    # def device_type_name(self):
    #     return self._dev_type_name

    @property
    def device_is_canfd(self):
        return self._dev_is_canfd

    @property
    def channels(self) -> tuple:
        return self._channels

    def _get_channel_handler(self, chl_type, channel):
        channels = self._channel_handlers[chl_type]
        return channels[channel]
        # return list(self._channel_handlers[chl_type].keys())[channel]

    def _get_can_init_config(self, mode, filter, **kwargs) -> ZCAN_CHANNEL_INIT_CONFIG:
        config = ZCAN_CHANNEL_INIT_CONFIG()
        assert self._dev_is_canfd is not None, f'The device{self._dev_index} is not opened!'
        config.can_type = ZCANCanType.CANFD if self._dev_is_canfd else ZCANCanType.CAN
        acc_code = kwargs.get('acc_code', 0)
        acc_mask = kwargs.get('acc_mask', 0xFFFFFFFF)
        if self._dev_is_canfd:
            # USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI acc_code, acc_mask ignored
            if self._dev_type not in ZUSBCANFD_TYPE:
                config.config.canfd.acc_code = acc_code
                config.config.canfd.acc_mask = acc_mask
            config.config.canfd.abit_timing = kwargs.get('abit_timing', 104286)     # ignored
            config.config.canfd.dbit_timing = kwargs.get('dbit_timing', 8487694)    # ignored
            config.config.canfd.brp = kwargs.get('brp', 0)
            config.config.canfd.filter = filter
            config.config.canfd.mode = mode
            config.config.canfd.brp = kwargs.get('pad', 0)
        else:
            if self._dev_type in (ZCANDeviceType.ZCAN_PCI5010U, ZCANDeviceType.ZCAN_PCI5020U,
                                  ZCANDeviceType.ZCAN_USBCAN_E_U, ZCANDeviceType.ZCAN_USBCAN_2E_U,
                                  ZCANDeviceType.ZCAN_USBCAN_4E_U, ZCANDeviceType.ZCAN_CANDTU_200UR,
                                  ZCANDeviceType.ZCAN_CANDTU_MINI, ZCANDeviceType.ZCAN_CANDTU_NET,
                                  ZCANDeviceType.ZCAN_CANDTU_100UR, ZCANDeviceType.ZCAN_CANDTU_NET_400):
                config.config.can.acc_code = acc_code
                config.config.can.acc_mask = acc_mask
            config.config.can.filter = filter
            if self._dev_type in ZUSBCAN_I_II_TYPE:
                config.config.can.timing0 = kwargs.get('timing0', 0)                   # ignored
                config.config.can.timing1 = kwargs.get('timing0', 28)                  # ignored
            config.config.can.mode = mode
        return config

    def _merge_support(self):
        if self._dev_type not in (ZCANDeviceType.ZCAN_USBCANFD_200U, ZCANDeviceType.ZCAN_USBCANFD_100U,
                                  ZCANDeviceType.ZCAN_USBCANFD_MINI, ZCANDeviceType.ZCAN_CANFDNET_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_UDP, ZCANDeviceType.ZCAN_CANFDNET_400U_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_400U_UDP, ZCANDeviceType.ZCAN_CANFDNET_100U_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_100U_UDP, ZCANDeviceType.ZCAN_CANFDNET_800U_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_800U_UDP, ZCANDeviceType.ZCAN_CANFDWIFI_TCP,
                                  ZCANDeviceType.ZCAN_CANFDWIFI_UDP, ZCANDeviceType.ZCAN_CANFDDTU_400_TCP,
                                  ZCANDeviceType.ZCAN_CANFDDTU_400_UDP, ZCANDeviceType.ZCAN_PCIE_CANFD_100U_EX,
                                  ZCANDeviceType.ZCAN_PCIE_CANFD_400U_EX, ZCANDeviceType.ZCAN_PCIE_CANFD_200U_MINI,
                                  ZCANDeviceType.ZCAN_PCIE_CANFD_200U_M2):
            raise ZCANException(f'ZLG: merge receive is not supported by {self._dev_type_name}!')

    def ResistanceStatus(self, channel, status=None):
        if status is not None:
            self.SetValue(channel, initenal_resistance=status)
        return self.GetValue(channel, 'initenal_resistance')

    def MergeEnabled(self):
        """
        设备是否开启合并收发模式
        :return: True if enabled else False
        """
        return self.GetValue(None, 'get_device_recv_merge/1') is not None

    # DEVICE_HANDLE FUNC_CALL ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
    def OpenDevice(self, dev_type: ZCANDeviceType, dev_index=0, reserved=0):
        ret = _library.ZCAN_OpenDevice(dev_type, dev_index, reserved)
        if ret == INVALID_DEVICE_HANDLE:
            raise ZCANException('ZLG: Open device failed!')
        self._dev_handler = ret
        self._dev_index = dev_index
        self._dev_type = dev_type
        # matched = re.findall(r'[.](\w*?),', inspect.getframeinfo(inspect.currentframe().f_back)[3][0])
        # assert len(matched) > 0
        # self._dev_type_name = matched[0]
        self._dev_info = self.GetDeviceInf()
        channels = self._dev_info.can_num
        self._channels = tuple(i for i in range(channels))
        self._dev_is_canfd = 'CANFD' in self._dev_info.hw_type

    # UINT FUNC_CALL ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
    def CloseDevice(self):
        can_channels = self._channel_handlers['CAN']
        lin_channels = self._channel_handlers['LIN']
        for index, _ in enumerate(can_channels):
            self.ResetCAN(index)
        for index, _ in enumerate(lin_channels):
            self.ResetLIN(index)
        ret = _library.ZCAN_CloseDevice(self._dev_handler)
        if ret != ZCAN_STATUS_OK:
            self._logger.warning(f'ZLG: Close device failed, code {ret}!')
        can_channels.clear()
        lin_channels.clear()
        self._dev_handler = None

    # UINT FUNC_CALL ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);
    def GetDeviceInf(self) -> ZCAN_DEVICE_INFO:
        dev_info = ZCAN_DEVICE_INFO()
        ret = _library.ZCAN_GetDeviceInf(self._dev_handler, byref(dev_info))
        if ret == ZCAN_STATUS_OK:
            return dev_info
        self._logger.warning(f'ZLG: Get device info failed, code {ret}!')

    # UINT FUNC_CALL ZCAN_IsDeviceOnLine(DEVICE_HANDLE device_handle);
    def DeviceOnLine(self):
        ret = _library.ZCAN_IsDeviceOnLine(self._dev_handler)
        self._logger.debug(f'ZLG: get device is online return code: {ret}.')
        return ret == ZCAN_STATUS_ONLINE

    # CHANNEL_HANDLE FUNC_CALL ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index, ZCAN_CHANNEL_INIT_CONFIG* pInitConfig);
    def InitCAN(self, channel, mode: ZCANCanMode = ZCANCanMode.NORMAL,
                filter: ZCANCanFilter = ZCANCanFilter.DOUBLE,
                **kwargs):
        """
        初始化CAN(FD)通道
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param mode: CAN(FD)模式, 可选值0: 正常模式, 1: 只听(只读)模式, 默认0
| mode        | 通道工作模式         | 0 - 正常模式 <br/> 1 - 只听模式 |     |
        :param filter: CAN(FD)滤波方式, 可选值0: 双滤波, 1: 单滤波, 默认0
        :param kwargs: 其他关键字参数, 说明如下:
| 名称          | 功能             | 值说明                     | 默认值 | 备注            |
|-------------|----------------|-------------------------|-----|---------------|
| acc_code    | SJA1000的帧过滤验收码 | 推荐设置为0x0                |     |               |
| acc_mask    | SJA1000的帧过滤屏蔽码 | 推荐设置为0xffffffff         |     |               |
| filter      | 滤波方式           | 0 - 双滤波 <br/> 1 - 单滤波   | 0   |               |
| brp         | 滤波预分频因子        | 设置为0                    |     | 仅CANFD, 影响波特率 |
| abit_timing | ignored        | NA                      | NA  | 仅CANFD        |
| dbit_timing | ignored        | NA                      | NA  | 仅CANFD        |

        :return: None
        """
        config = self._get_can_init_config(mode, filter, **kwargs)
        ret = _library.ZCAN_InitCAN(self._dev_handler, channel, byref(config))
        if ret == INVALID_CHANNEL_HANDLE:
            raise ZCANException('ZLG: Can Channel initialize failed!')
        self._logger.debug(f'ZLG: channel{channel} handler: {ret}')
        # self._channel_handlers['CAN'][ret] = can_type == ZlgCanType.CANFD
        self._channel_handlers['CAN'].append(ret)

    # UINT FUNC_CALL ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
    def StartCAN(self, channel):
        handler = self._get_channel_handler('CAN', channel)
        ret = _library.ZCAN_StartCAN(handler)
        if ret != ZCAN_STATUS_OK:
            raise ZCANException('ZLG: Can Channel start failed!')

    # UINT FUNC_CALL ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
    def ResetCAN(self, channel):
        handler = self._get_channel_handler('CAN', channel)
        ret = _library.ZCAN_ResetCAN(handler)
        if ret != ZCAN_STATUS_OK:
            raise ZCANException('ZLG: Can Channel reset failed!')

    # UINT FUNC_CALL ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
    def ClearBuffer(self, channel):
        handler = self._get_channel_handler('CAN', channel)
        ret = _library.ZCAN_ClearBuffer(handler)
        if ret != ZCAN_STATUS_OK:
            raise ZCANException('ZLG: Can Channel reset failed!')

    # UINT FUNC_CALL ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
    def ReadChannelErrInfo(self, channel, chl_type='CAN'):
        handler = self._get_channel_handler(chl_type, channel)
        error_info = ZCAN_CHANNEL_ERR_INFO()
        ret = _library.ZCAN_ReadChannelErrInfo(handler, byref(error_info))
        if ret == ZCAN_STATUS_OK:
            return error_info
        self._logger.warning(f'ZLG: Read channel error info failed, code {ret}!')

    # UINT FUNC_CALL ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
    def ReadChannelStatus(self, channel, chl_type='CAN'):
        warnings.warn('ZLG: no device supported.', DeprecationWarning, 2)
        handler = self._get_channel_handler(chl_type, channel)
        status_info = ZCAN_CHANNEL_STATUS()
        ret = _library.ZCAN_ReadChannelStatus(handler, byref(status_info))
        if ret == ZCAN_STATUS_OK:
            return status_info
        self._logger.warning(f'ZLG: Read channel status info failed, code {ret}!')

    # UINT FUNC_CALL ZCAN_GetLINReceiveNum(CHANNEL_HANDLE channel_handle);
    # UINT FUNC_CALL ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);//type:TYPE_CAN, TYPE_CANFD, TYPE_ALL_DATA
    def GetReceiveNum(self, channel, msg_type: ZCANMessageType = ZCANMessageType.CAN):
        """
        获取指定通道已经接收到消息数量
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msg_type: 消息类型: 0 - CAN; 1 - CANFD; '-1' - LIN
        :return: 消息数量
        """
        if msg_type == ZCANMessageType.LIN:
            return _library.ZCAN_GetLINReceiveNum(self._get_channel_handler('LIN', channel))
        return _library.ZCAN_GetReceiveNum(self._get_channel_handler('CAN', channel), msg_type)

    def TransmitCan(self, channel, msgs, size=None):
        handler = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = _library.ZCAN_Transmit(handler, byref(msgs), _size)
        return ret

    def ReceiveCan(self, channel, size=1, timeout=-1):
        handler = self._get_channel_handler('CAN', channel)
        can_msgs = (ZCAN_Receive_Data * size)()
        ret = _library.ZCAN_Receive(handler, byref(can_msgs), size, timeout)
        return can_msgs, ret

    def TransmitFD(self, channel, msgs, size=None):
        handler = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = _library.ZCAN_TransmitFD(handler, byref(msgs), _size)
        return ret

    def ReceiveFD(self, channel, size=1, timeout=-1):
        handler = self._get_channel_handler('CAN', channel)
        can_msgs = (ZCAN_ReceiveFD_Data * size)()
        ret = _library.ZCAN_ReceiveFD(handler, byref(can_msgs), size, timeout)
        return can_msgs, ret

    # # UINT FUNC_CALL ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
    # UINT FUNC_CALL ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
    def Transmit(self, channel, msgs, size=None):
        """
        发送CAN(FD)报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msgs: 消息报文
        :param size: 报文大小
        :return:
        """
        handler = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = _library.ZCAN_Transmit(handler, byref(msgs), _size)
        return ret

    # UINT FUNC_CALL ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, int wait_time DEF(-1));
    # UINT FUNC_CALL ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, int timeout DEF(-1));
    def Receive(self, channel, size=1, timeout=-1):
        """
        接收CAN(FD)报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param size: 期待接收报文个数
        :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
        :return: 消息内容及消息实际长度
        """
        handler = self._get_channel_handler('CAN', channel)
        can_msgs = (ZCAN_Receive_Data * size)()
        ret = _library.ZCAN_Receive(handler, byref(can_msgs), size, timeout)
        return can_msgs, ret

    # UINT FUNC_CALL ZCAN_TransmitData(DEVICE_HANDLE device_handle, ZCANDataObj* pTransmit, UINT len);
    def TransmitData(self, msgs, size=None):
        """
        合并发送数据[只有在设备支持合并发送功能并开启合并发送功能后才可以正常的发送到各种数据]
        :param msgs: 消息内容
        :param size: 消息长度
        :return: 实际发送的消息长度
        """
        self._merge_support()
        _size = size or len(msgs)
        ret = _library.ZCAN_TransmitData(self._dev_handler, byref(msgs), _size)
        return ret

    # UINT FUNC_CALL ZCAN_ReceiveData(DEVICE_HANDLE device_handle, ZCANDataObj* pReceive, UINT len, int wait_time DEF(-1));
    def ReceiveData(self, size=1, timeout=-1):
        """
        合并接收数据[只有在设备支持合并接收功能并开启合并接收功能后才可以正常的接收到各种数据]
        :param size: 期待接收的数据大小
        :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
        :return: 消息内容及消息实际长度
        """
        # warnings.warn('ZLG: Library not support.', DeprecationWarning, 2)
        # self.zlg_get_property()
        self._merge_support()
        if not self.MergeEnabled():
            raise ZCANException('ZLG: device merge receive is not enable!')
        msgs = (ZCANDataObj * size)()
        ret = _library.ZCAN_ReceiveData(self._dev_handler, byref(msgs), size, c_int(timeout))
        return msgs, ret

    # IProperty* FUNC_CALL GetIProperty(DEVICE_HANDLE device_handle);
    def GetIProperty(self):
        _library.GetIProperty.restype = POINTER(IProperty)
        return _library.GetIProperty(self._dev_handler)

    # UINT FUNC_CALL ReleaseIProperty(IProperty * pIProperty);
    def ReleaseIProperty(self, prop: IProperty):
        return _library.ReleaseIProperty(prop)

    def SetAutoTransmit(self, channel, auto_tran: ZCAN_AUTO_TRANSMIT_OBJ, delay: ZCANFD_AUTO_TRANSMIT_OBJ_PARAM):
        prop = self.GetIProperty()
        try:
            func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(prop.contents.SetValue)
            ret = func(c_char_p(f'{channel}/clear_auto_send'.encode("utf-8")), c_char_p('0'.encode('utf-8')))
            if ret != ZCAN_STATUS_OK:
                raise ZCANException(f'ZLG: Set {channel}/clear_auto_send failed!')
            func1 = CFUNCTYPE(c_uint, c_char_p, c_void_p)(prop.contents.SetValue)
            ret = func1(c_char_p(f'{channel}/'.encode("utf-8")), cast(byref(auto_tran), c_void_p))
            if ret != ZCAN_STATUS_OK:
                raise ZCANException(f'ZLG: Set {channel} auto transmit object failed!')
            ret = func1(c_char_p(f'{channel}/'.encode("utf-8")), cast(byref(delay), c_void_p))
            if ret != ZCAN_STATUS_OK:
                raise ZCANException(f'ZLG: Set {channel} auto transmit object param failed!')
            ret = func(c_char_p(f'{channel}/apply_auto_send'.encode("utf-8")), c_char_p('0'.encode('utf-8')))
            if ret != ZCAN_STATUS_OK:
                raise ZCANException(f'ZLG: Set {channel}/apply_auto_send failed!')
        finally:
            self.ReleaseIProperty(prop)

    # UINT FUNC_CALL ZCAN_SetValue(DEVICE_HANDLE device_handle, const char* path, const void* value);
    def SetValue(self, channel, **kwargs):
        """
        设置通道波特率/时钟频率/终端电阻使能等属性信息
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param kwargs: 其他关键字参数/字典:
| 名称                              | 参数功能                             | 值说明                                                                              | 默认值                   | 时机                     | 备注                                                                  |
|---------------------------------|----------------------------------|----------------------------------------------------------------------------------|-----------------------|------------------------|---------------------------------------------------------------------|
| canfd_standard                  | 设置协议类型                           | 0 – CANFD ISO <br/> 1 – CANFD Non-ISO                                            | CANFD ISO 类型          | 需在 init_channel 之前设置   | 适用USBCANFD-100U 、USBCANFD-200U 、USBCANFD-MINI 设备                    |
| protocol                        | 设置协议类型                           | 0 – CAN <br/> 1 – CANFD ISO <br/> 2 – CANFD Non-ISO                              | CANFD ISO 类型          | 需在 init_channel 之前设置   | 适用 USBCANFD-800U 设备                                                 |
| clock                           | 设置时钟频率, 直接影响波特率                  | 不同设备支持的时钟频率不同                                                                    | 上一次设置值                | 在设置波特率之前               |                                                                     |
| canfd_abit_baud_rate            | 设置仲裁域波特率                         | 1000000,800000,500000, <br/> 250000,125000,100000,50000                          | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| canfd_dbit_baud_rate            | 设置数据域波特率                         | 5000000,4000000,2000000, <br/> 1000000,800000,500000, <br/> 250000,125000,100000 | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| baud_rate_custom                | 设置自定义波特率                         | 需计算                                                                              | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| initenal_resistance             | 设置终端电阻                           | 0 - 禁能 <br/> 1 - 使能                                                              | 上一次设置值                | 需在 init_channel 之后设置   |                                                                     |
| tx_timeout                      | 设置发送超时时间                         | 0 ~ 4000 ms                                                                      |                       |                        | 只适用 100U/200U/MINI/设备、不适用 USBCANFD-800U                             |
| auto_send                       | 设置定时发送CAN 帧                      |                                                                                  |                       | 需在 start_channel 之后设置  |                                                                     |
| auto_send_canfd                 | 设置定时发送 CANFD 帧                   |                                                                                  |                       | 需在 start_channel 之后设置  | USBCANFD 支持每通道最大 100 条定时发送列表（USBCANFD-800U 支持每通道最大 32条定时发送列表）       |
| auto_send_param                 | 定时发送附加参数（用于设定特定索引定时发送帧的延时启动）     |                                                                                  | 需在 start_channel 之后设置 | 需在 start_channel 之后设置  | 适用 USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI 设备，USBCANFD-800U 不适用   |
| clear_auto_send                 | 清空定时发送                           | 0 - 固定值                                                                          |                       | 需在 start_channel 之后设置  |                                                                     |
| apply_auto_send                 | 应用定时发送（使能定时发送属性设置）               | 0 - 固定值                                                                          |                       | 需在 start_channel 之后设置  |                                                                     |
| set_send_mode                   | 设置设备发送模式                         | 0 – 正常模式 <br/> 1 – 队列模式                                                          | 0 正常模式                |                        | 适用 USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI 设备，USBCANFD-800U 不适用   |
| get_device_available_tx_count/1 | 获取发送队列可用缓存数量（仅队列模式）              | 无                                                                                |                       |                        | 最后的数字“1”只是内部标志，可以是任意数字                                              |
| clear_delay_send_queue          | 清空发送缓存（仅队列模式，缓存中未发送的帧将被清空，停止时使用） | 0 - 固定值                                                                          |                       |                        |                                                                     |
| set_device_recv_merge           | 设置合并接收功能开启/关闭                    | 0 – 关闭合并接收功能 <br/> 1 – 开启合并接收功能                                                  | 0 – 关闭合并接收功能          |                        |                                                                     |
| get_device_recv_merge/1         | 获取设备当前是否开启了合并接收                  | 无                                                                                |                       |                        | 最后的数字“1”只是内部标志，可以是任意数字                                              |
| set_cn                          | 设置自定义序列号                         | 自定义字符串, 最多 128 字符                                                                |                       |                        | 适用 USBCANFD-100U 、USBCANFD-200U、USBCANFD-MINI 设备                    |
| set_name                        | 设置自定义序列号                         | 自定义字符串, 最多 128 字符                                                                |                       |                        | 适用 USBCANFD-800U 设备                                                 |
| get_cn/1                        | 获取自定义序列号                         | 无                                                                                |                       |                        | 适用 USBCANFD-100U 、USBCANFD-200U、USBCANFD-MINI 设备, 后面的 1 必须，也可以是任意数字 |
| get_name/1                      | 获取自定义序列号                         |                                                                                  |                       |                        | 适用 USBCANFD-800U 设备, 后面的 1 必须，也可以是任意数字                              |
| filter_mode                     | 设置滤波模式                           | 0 – 标准帧 <br/> 1 – 扩展帧                                                            |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_start                    | 设置滤波起始帧 ID                       | 16 进制字符如: 0x00000000                                                             |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_end                      | 设置滤波结束帧 ID                       | 16 进制字符如: 0x00000000                                                             |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_ack                      | 滤波生效（全部滤波 ID 同时生效）               | 0 - 固定值                                                                          |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_clear                    | 清除滤波                             | 0 - 固定值                                                                          |                       | 需在 init_channel 之后设置   |                                                                     |
| set_bus_usage_enable            | 设置总线利用率信息上报开关                    | 0 - 禁能 <br/> 1 - 使能                                                              |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备                                                |
| set_bus_usage_period            | 设置总线利用率信息上报周期                    | 20 ~ 2000 ms                                                                     |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备                                                |
| get_bus_usage/1                 | 获取总线利用率信息                        | 无                                                                                |                       | 	需在 start_channel 之后获取 | 只适用 USBCANFD-800U 设备, 最后的数字“1”只是内部标志，可以是任意数字                        |
| set_tx_retry_policy             | 设置发送失败时重试策略                      | 0 – 发送失败不重传 <br/> 1 -发送失败重传，直到总线关闭                                               |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备，其他 USBCANFD 设备通过设置工作模式来写入属性                    |

        :return: None
        """
        prop = self.GetIProperty()
        try:
            for path, value in kwargs.items():
                func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(prop.contents.SetValue)
                # _path = f'{channel}/{path}' if channel else f'{path}'
                ret = func(c_char_p(_path(channel, path).encode("utf-8")), c_char_p(f'{value}'.encode("utf-8")))
                if ret != ZCAN_STATUS_OK:
                    raise ZCANException(f'ZLG: Set channel{channel} property: {path} = {value} failed, code {ret}!')
                self._logger.debug(f'ZLG: Set channel{channel} property: {path} = {value} success.')
                assert str(value) == self.GetValue(channel, path, prop)
        finally:
            self.ReleaseIProperty(prop)

    # const void* FUNC_CALL ZCAN_GetValue(DEVICE_HANDLE device_handle, const char* path);
    def GetValue(self, channel, path, prop=None) -> str:
        """
        获取属性值
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param path: 参考zlg_set_properties说明中的字典参数
        :param prop: 属性对象, None即可(内部调用使用)
        :return: 属性值
        """
        _prop = prop or self.GetIProperty()
        try:
            func = CFUNCTYPE(c_char_p, c_char_p)(_prop.contents.GetValue)
            # _path = f'{channel}/{path}' if channel else f'{path}'
            ret = func(c_char_p(_path(channel, path).encode("utf-8")))
            if ret:
                return ret.decode('utf-8')
        finally:
            if not prop:
                self.ReleaseIProperty(_prop)

    # void FUNC_CALL ZCLOUD_SetServerInfo(const char* httpSvr, unsigned short httpPort, const char* authSvr, unsigned short authPort);
    def SetServerInfo(self, auth_host: str, auth_port, data_host=None, data_post=None):
        ret = _library.ZCLOUD_SetServerInfo(c_char_p(auth_host.encode('utf-8')), c_ushort(auth_port),
                                            c_char_p((data_host or auth_host).encode('utf-8')),
                                            c_ushort(data_post or auth_port))
        if ret != ZCAN_STATUS_OK:
            raise ZCANException(f'ZLG: set server info failed!')

    # // return 0:success, 1:failure, 2:https error, 3:user login info error, 4:mqtt connection error, 5:no device
    # UINT FUNC_CALL ZCLOUD_ConnectServer(const char* username, const char* password);
    def ConnectServer(self, username, password):
        ret = _library.ZCLOUD_ConnectServer(c_char_p(username.encode('utf-8')), c_char_p(password.encode('utf-8')))
        if ret == 0:
            return
        elif ret == 1:
            raise ZCANException('ZLG: connect server failure')
        elif ret == 2:
            raise ZCANException('ZLG: connect server https error')
        elif ret == 3:
            raise ZCANException('ZLG: connect server user login info error')
        elif ret == 4:
            raise ZCANException('ZLG: connect server mqtt connection error')
        elif ret == 5:
            raise ZCANException('ZLG: connect server no device')
        else:
            raise ZCANException(f'ZLG: connect server undefined error: {ret}')

    # bool FUNC_CALL ZCLOUD_IsConnected();
    def CloudConnected(self):
        return _library.ZCLOUD_IsConnected()

    # // return 0:success, 1:failure
    # UINT FUNC_CALL ZCLOUD_DisconnectServer();
    def DisconnectServer(self):
        ret = _library.ZCLOUD_IsConnected()
        return ret == 0

    # const ZCLOUD_USER_DATA* FUNC_CALL ZCLOUD_GetUserData(int update DEF(0));
    def GetUserData(self, userid) -> ZCLOUD_USER_DATA:
        return _library.ZCLOUD_GetUserData(userid)

    # UINT FUNC_CALL ZCLOUD_ReceiveGPS(DEVICE_HANDLE device_handle, ZCLOUD_GPS_FRAME* pReceive, UINT len, int wait_time DEF(-1));
    def ReceiveGPS(self, size=1, timeout=-1):
        msgs = (ZCLOUD_GPS_FRAME * size)()
        ret = _library.ZCLOUD_ReceiveGPS(self._dev_handler, byref(msgs), size, timeout)
        return msgs, ret

    # CHANNEL_HANDLE FUNC_CALL ZCAN_InitLIN(DEVICE_HANDLE device_handle, UINT can_index, PZCAN_LIN_INIT_CONFIG pLINInitConfig);
    def InitLIN(self, channel, config: ZCAN_LIN_INIT_CONFIG):
        ret = _library.ZCAN_InitLIN(self._dev_handler, channel, byref(config))
        if ret == INVALID_CHANNEL_HANDLE:
            raise ZCANException('ZLG: Lin Channel initialize failed!')
        self._channel_handlers['LIN'][ret] = True

    # UINT FUNC_CALL ZCAN_StartLIN(CHANNEL_HANDLE channel_handle);
    def StartLIN(self, channel):
        handler = self._get_channel_handler('LIN', channel)
        ret = _library.ZCAN_StartLIN(handler)
        if ret != ZCAN_STATUS_OK:
            raise ZCANException(f'ZLG: Lin Channel start failed, code {ret}!')

    # UINT FUNC_CALL ZCAN_ResetLIN(CHANNEL_HANDLE channel_handle);
    def ResetLIN(self, channel):
        handler = self._get_channel_handler('LIN', channel)
        ret = _library.ZCAN_ResetLIN(handler)
        if ret != ZCAN_STATUS_OK:
            raise ZCANException(f'ZLG: Lin Channel reset failed, code {ret}!')

    # UINT FUNC_CALL ZCAN_TransmitLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT Len);
    def TransmitLIN(self, channel, msgs, size=None):
        handler = self._get_channel_handler('LIN', channel)
        _size = size or len(msgs)
        ret = _library.ZCAN_TransmitLIN(handler, byref(msgs), _size)
        if ret != ZCAN_STATUS_OK:
            raise ZCANException(f'ZLG: Clear Lin master write failed, code {ret}!')

    # UINT FUNC_CALL ZCAN_ReceiveLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pReceive, UINT Len,int WaitTime);
    def ReceiveLIN(self, channel, size=1, timeout=-1):
        msgs = (ZCAN_LIN_MSG * size)()
        handler = self._get_channel_handler('LIN', channel)
        ret = _library.ZCAN_ReceiveLIN(handler, byref(msgs), size, c_int(timeout))
        return msgs, ret

    # UINT FUNC_CALL ZCAN_SetLINSlaveMsg(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT nMsgCount);
    def SetLINSlaveMsg(self, channel, msgs):
        handler = self._get_channel_handler('LIN', channel)
        ret = _library.ZCAN_SetLINSlaveMsg(handler, byref(msgs), len(msgs))
        if ret != ZCAN_STATUS_OK:
            raise ZCANException(f'ZLG: Clear Lin slave write failed, code {ret}!')

    # UINT FUNC_CALL ZCAN_ClearLINSlaveMsg(CHANNEL_HANDLE channel_handle, BYTE* pLINID, UINT nIDCount);
    def ClearLINSlaveMsg(self, channel, lin_ids):
        handler = self._get_channel_handler('LIN', channel)
        ret = _library.ZCAN_ClearLINSlaveMsg(handler, byref(lin_ids), len(lin_ids))
        # self._logger.debug(f'ZLG: Clear Lin slave message return code {ret}.')
        if ret != ZCAN_STATUS_OK:
            raise ZCANException(f'ZLG: Clear Lin slave message failed, code {ret}!')










