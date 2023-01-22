import sys
import time

import aiohttp
import yarl

from .._core import APP_BASE_HOST, TbCore
from .._exception import TiebaServerError
from .._helper import APP_SECURE_SCHEME, log_exception, log_success, pack_form_request, parse_json, send_request


def parse_body(body: bytes) -> None:
    res_json = parse_json(body)
    if code := int(res_json['error_code']):
        raise TiebaServerError(code, res_json['error_msg'])


async def request(connector: aiohttp.TCPConnector, core: TbCore, fid: int) -> bool:

    data = [
        ('BDUSS', core._BDUSS),
        ('_client_version', core.main_version),
        (
            'dislike',
            f"""[{{"tid": 1, "dislike_ids": 7, "fid": {fid}, "click_time": {int(time.time() * 1000)}}}]""",
        ),
        ('dislike_from', "homepage"),
    ]

    request = pack_form_request(
        core,
        yarl.URL.build(scheme=APP_SECURE_SCHEME, host=APP_BASE_HOST, path="/c/c/excellent/submitDislike"),
        data,
    )

    log_str = f"fid={fid}"
    frame = sys._getframe(1)

    try:
        body = await send_request(request, connector, read_bufsize=1024)
        parse_body(body)

    except Exception as err:
        log_exception(frame, err, log_str)
        return False

    log_success(frame, log_str)
    return True
