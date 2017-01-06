from django.db import models
from django.conf import settings

from blog.models import Post

class Comment(models.Model):
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    post        = models.ForeignKey(Post)
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author.get_full_name())