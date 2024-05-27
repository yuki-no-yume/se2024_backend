from django.db import models


class DataDescriptionImage(models.Model):
    belongs2id = models.IntegerField()
    image_url = models.CharField(primary_key=True, max_length=128)

    class Meta:
        db_table = "data_description_images"
        managed = False

    def to_dict(self) -> dict:
        return {
            "belongs2id": self.belongs2id,
            "image_url": self.image_url,
        }
