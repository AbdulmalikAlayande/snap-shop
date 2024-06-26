from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model, CharField, CASCADE, ForeignKey


# Create your models here.

class Tag(Model):
    label = CharField(max_length=255)

    def __repr__(self):
        return f'{self.label}'


class Tagged_Item(Model):
    tag = ForeignKey(to=Tag, on_delete=CASCADE)
    content_type = ForeignKey(to=ContentType, on_delete=CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __repr__(self):
        return "{}, {}, {}, {}".format(self.tag, self.tag_id, self.object_id, self.content_object)

