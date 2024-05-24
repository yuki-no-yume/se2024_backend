import os
import random
from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST

from utils.response_util import *

DATA_PATH = "./file/data"
IMAGES_PATH = "./file/images"


def _file_rename(origin_name: str, is_data: bool = False) -> str:
    character_set = [chr(i) for i in list(range(65, 91)) + list(range(97, 123)) + list(range(48, 58))]
    datestamp = datetime.now().strftime("%Y%m%d")
    name_rand = "".join(random.sample(character_set, 12))
    if "." in origin_name:
        suffix = origin_name.split(".")[-1]
        rename = f"{datestamp}-{name_rand}.{suffix}" if is_data else f"{name_rand}.{suffix}"
    else:
        rename = f"{datestamp}-{name_rand}" if is_data else f"{name_rand}"
    if (is_data and rename in os.listdir(DATA_PATH)) or (not is_data and rename in os.listdir(IMAGES_PATH)):
        return _file_rename(origin_name, is_data=is_data)
    return rename


@require_POST
def file_upload(request: HttpRequest):
    # TODO: 检查权限
    file = request.FILES.get("file")
    rename = _file_rename(file.name, is_data=True)
    with open(f"{DATA_PATH}/{rename}", "wb") as f:
        f.write(file.file.read())
    return build_success_json_response({"file_url": f"{DATA_PATH}/{rename}"})
