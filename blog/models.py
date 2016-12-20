from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    """
    you're going to allow a field to be blank in your form,
    you're going to also need your database to allow NULL values for that field.
    The exception is CharFields and TextFields, which in Django are never saved as NULL.
    Blank values are stored in the DB as an empty string ('').
    """

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "b/{}/".format(self.id)
        return reverse('posts:detail', kwargs={'id': self.id})