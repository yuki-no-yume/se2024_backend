from django.db import models

from .data_description_image import DataDescriptionImage


class DownloadItem(models.Model):
    file_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    file_url = models.CharField(max_length=128)

    class Meta:
        db_table = "download_items"
        managed = False

    def to_dict(self) -> dict:
        image_urls = []
        image_set = DataDescriptionImage.objects.filter(belongs2id=self.file_id)
        for elm in image_set:
            image_urls.append(elm.image_url)
        return {
            "file_id": self.file_id,
            "title": self.title,
            "description": self.description,
            "data_url": self.file_url,
            "image_urls": image_urls,
        }
