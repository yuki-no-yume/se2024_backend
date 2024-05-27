import os
import random
from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST

from utils.response_util import *
from ylqk.models import DownloadItem, DataDescriptionImage

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
    title = request.POST.get("title")
    description = request.POST.get("description")
    file = request.FILES.get("file")
    images = request.FILES.getlist("images")

    file_rename = _file_rename(file.name, is_data=True)
    file_url = f"{DATA_PATH}/{file_rename}"
    with open(file_url, "wb") as f:
        f.write(file.file.read())
    DownloadItem.objects.create(
        title=title,
        description=description,
        file_url=file_url,
    )
    download_item = DownloadItem.objects.filter(file_url=file_url).first()

    for upload_image in images:
        image_rename = _file_rename(upload_image.name)
        image_url = f"{IMAGES_PATH}/{image_rename}"
        with open(image_url, "wb") as image:
            image.write(upload_image.file.read())
        DataDescriptionImage.objects.create(
            belongs2id=download_item.item_id,
            image_url=image_url,
        )
    return build_success_json_response(message="文件上传成功")


@require_POST
def file_delete(request: HttpRequest):
    # TODO: 检查权限
    item_id = request.POST.get("item_id")
    DataDescriptionImage.objects.filter(belongs2id=item_id).delete()
    DownloadItem.objects.filter(item_id=item_id).delete()
    return build_success_json_response(message="文件删除成功")
