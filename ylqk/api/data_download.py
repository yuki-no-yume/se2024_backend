import os
import random
from datetime import datetime
from django.http import HttpRequest, FileResponse
from django.views.decorators.http import require_POST, require_GET

from utils.response_util import *
from ylqk.models import DownloadItem, DataDescriptionImage

ROOT_PATH = "/root/SE2024/se2024_backend/"
DATA_PATH = "file/data"
IMAGES_PATH = "file/images"
PAGE_SIZE = 10


def _file_rename(origin_name: str, is_data: bool = False) -> str:
    character_set = [chr(i) for i in list(range(65, 91)) + list(range(97, 123)) + list(range(48, 58))]
    datestamp = datetime.now().strftime("%Y%m%d")
    name_rand = "".join(random.sample(character_set, 12))
    if "." in origin_name:
        suffix = origin_name.split(".")[-1]
        rename = f"{datestamp}-{name_rand}.{suffix}" if is_data else f"{name_rand}.{suffix}"
    else:
        rename = f"{datestamp}-{name_rand}" if is_data else f"{name_rand}"
    if (is_data and rename in os.listdir(ROOT_PATH + DATA_PATH)) or \
            (not is_data and rename in os.listdir(ROOT_PATH + IMAGES_PATH)):
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
    file_url = f"{ROOT_PATH + DATA_PATH}/{file_rename}"
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
        with open(ROOT_PATH + image_url, "wb") as image:
            image.write(upload_image.file.read())
        DataDescriptionImage.objects.create(
            belongs2id=download_item.file_id,
            image_url=image_url,
        )
    return build_success_json_response(message="文件上传成功")


@require_POST
def file_delete(request: HttpRequest):
    # TODO: 检查权限
    file_id = request.POST.get("file_id")
    DataDescriptionImage.objects.filter(belongs2id=file_id).delete()
    DownloadItem.objects.filter(file_id=file_id).delete()
    return build_success_json_response(message="文件删除成功")


@require_GET
def file_search(request: HttpRequest):
    keyword = request.GET.get("keyword")
    page = int(request.GET.get("page")) if request.GET.get("page") is not None and request.GET.get("page") != "" else 1
    if keyword is not None and keyword != "":
        item_all = DownloadItem.objects.filter(title__icontains=keyword)
    else:
        item_all = DownloadItem.objects.all()
    if (page - 1) * PAGE_SIZE <= len(item_all):
        cur_page = page
        item_sub = item_all[(page - 1) * PAGE_SIZE:page * PAGE_SIZE]
    else:
        cur_page = int(len(item_all) / PAGE_SIZE)
        item_sub = item_all[cur_page * PAGE_SIZE:]
    files = []
    for elm in item_sub:
        files.append(elm.to_dict())
    return build_success_json_response({
        "page": cur_page,
        "files": files,
    })


@require_GET
def file_download(request: HttpRequest):
    file_id = request.GET.get("file_id")
    download_item = DownloadItem.objects.filter(file_id=file_id).first()
    if download_item is None:
        return build_failed_json_response(StatusCode.NOT_FOUND, message="文件不存在")
    file = open(download_item.file_url, "rb")
    response = FileResponse(file, as_attachment=True)
    return response
