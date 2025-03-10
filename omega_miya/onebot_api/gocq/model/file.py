"""
@Author         : Ailitonia
@Date           : 2022/04/16 14:49
@FileName       : file.py
@Project        : nonebot2_miya 
@Description    : go-cqhttp File Model
@GitHub         : https://github.com/Ailitonia
@Software       : PyCharm 
"""

from typing import Optional
from pydantic import AnyHttpUrl, Field
from ...model import BaseOnebotModel
from ...model import VersionInfo as OnebotVersionInfo
from ...model import Cookies as OnebotCookies, CSRF as OnebotCSRF, Credentials as OnebotCredentials
from ...model import RecordFile as OnebotRecordFile
from ...model import CanSendImage as OnebotCanSendImage, CanSendRecord as OnebotCanSendRecord
from ...model import Status as OnebotStatus


class Cookies(OnebotCookies):
    """Cookies"""


class CSRF(OnebotCSRF):
    """CSRF Token"""


class Credentials(OnebotCredentials):
    """Cookies 和 CSRF Token"""


class ImageFile(BaseOnebotModel):
    """图片文件

    - size: 图片源文件大小
    - filename: 图片文件原名
    - url: 图片下载地址
    """
    size: int
    filename: str
    url: AnyHttpUrl


class OcrImageResult(BaseOnebotModel):
    """图片 OCR 结果

    - texts: OCR结果
    - language: 语言
    """

    class _TextDetection(BaseOnebotModel):
        """OCR 文本内容

        - text: 文本
        - confidence: 置信度
        - coordinates: 坐标
        """

        class _Vector2(BaseOnebotModel):
            x: int
            y: int

        text: str
        confidence: int
        coordinates: list[_Vector2]

    texts: list[_TextDetection]
    language: str


class CanSendImage(OnebotCanSendImage):
    """是否可以发送图片"""


class RecordFile(OnebotRecordFile):
    """语音文件"""


class CanSendRecord(OnebotCanSendRecord):
    """是否可以发送语音"""


class DownloadedFile(BaseOnebotModel):
    """下载的文件"""
    file: str


class VersionInfo(OnebotVersionInfo):
    """go-cqhttp 版本信息

    - app_name: 应用标识, 如 go-cqhttp 固定值
    - app_version: 应用版本, 如 v0.9.40-fix4
    - app_full_name: 应用完整名称
    - protocol_version: OneBot 标准版本 固定值
    - coolq_edition: 原 Coolq 版本 固定值
    - coolq_directory: 原 Coolq 路径 固定值
    - go-cqhttp: 是否为go-cqhttp 固定值
    - plugin_version: 固定值
    - plugin_build_number: 固定值
    - plugin_build_configuration: 固定值
    - runtime_version
    - runtime_os
    - version: 应用版本, 如 v0.9.40-fix4
    - protocol: 当前登陆使用协议类型
    """
    is_go_cqhttp: bool = Field(default=True, alias='go-cqhttp')
    app_full_name: Optional[str]
    coolq_edition: Optional[str]
    coolq_directory: Optional[str]
    plugin_version: Optional[str]
    plugin_build_number: Optional[int]
    plugin_build_configuration: Optional[str]
    runtime_version: Optional[str]
    runtime_os: Optional[str]
    version: Optional[str]
    protocol: Optional[int] = Field(alias='protocol_name')

    class Config:
        extra = 'ignore'


class Status(OnebotStatus):
    """go-cqhttp 状态

    - app_initialized: 原 CQHTTP 字段, 恒定为 true
    - app_enabled: 原 CQHTTP 字段, 恒定为 true
    - plugins_good: 原 CQHTTP 字段, 恒定为 true(当前版本实际恒定为 None)
    - app_good: 原 CQHTTP 字段, 恒定为 true
    - online: 表示BOT是否在线
    - good: 同 online
    - stat: 运行统计
    """

    class _Statistics(BaseOnebotModel):
        """统计信息

        - PacketReceived: 收到的数据包总数
        - PacketSent: 发送的数据包总数
        - PacketLost: 数据包丢失总数
        - MessageReceived: 接受信息总数
        - MessageSent: 发送信息总数
        - DisconnectTimes: TCP 链接断开次数
        - LostTimes: 账号掉线次数
        - LastMessageTime: 最后一条消息时间
        """
        PacketReceived: int
        PacketSent: int
        PacketLost: int
        MessageReceived: int
        MessageSent: int
        DisconnectTimes: int
        LostTimes: int
        LastMessageTime: int

    app_initialized: Optional[bool]
    app_enabled: Optional[bool]
    plugins_good: Optional[bool]
    app_good: Optional[bool]
    stat: _Statistics

    class Config:
        extra = 'ignore'


class OnlineDevice(BaseOnebotModel):
    """在线客户端

    - app_id: 客户端ID
    - device_name: 设备名称
    - device_kind: 设备类型
    """
    app_id: int
    device_name: str
    device_kind: str


class OnlineClients(BaseOnebotModel):
    """当前账号在线客户端列表"""
    clients: list[OnlineDevice]


class UrlSafely(BaseOnebotModel):
    """链接安全性

    - level: 安全等级, 1: 安全 2: 未知 3: 危险
    """
    level: int


__all__ = [
    'Cookies',
    'CSRF',
    'Credentials',
    'ImageFile',
    'OcrImageResult',
    'CanSendImage',
    'RecordFile',
    'CanSendRecord',
    'DownloadedFile',
    'VersionInfo',
    'Status',
    'OnlineClients',
    'UrlSafely'
]
