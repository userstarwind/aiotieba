from __future__ import annotations

from .crypto import TypePayload, c3_aid, cuid_galaxy2, rc4_42
from .crypto import sign as _sign


def sign(data: TypePayload) -> TypePayload:
    """
    为参数元组列表添加贴吧客户端签名

    Args:
        data (list[tuple[str, str | int]]): 参数元组列表

    Returns:
        list[tuple[str, str | int]]: 签名后的form参数元组列表
    """

    data.append(('sign', _sign(data)))
    return data
