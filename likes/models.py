from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model, CASCADE, ForeignKey, PositiveIntegerField


# Create your models here.

class Liked_Item(Model):
    user = ForeignKey(to=User, on_delete=CASCADE)
    content_type = ForeignKey(to=ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    object_content = GenericForeignKey()
