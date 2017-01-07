from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentManager(models.Manager):
    def filter_by_instance(self, object):
        content_type = ContentType.objects.get_for_model(object.__class__)
        obj_id = object.id  # = Post.objects.get(id=object.id)
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class Comment(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')

    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.author.get_full_name())