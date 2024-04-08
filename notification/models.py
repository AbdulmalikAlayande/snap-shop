from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import ForeignKey, PositiveIntegerField, CASCADE


# Create your models here.

class Notification(models.Model):
    content_type = ForeignKey(to=ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    object_content = GenericForeignKey()

    class Meta:
        db_table = 'notifications'
