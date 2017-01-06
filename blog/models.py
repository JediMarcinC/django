from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.conf import settings

from markdown_deux import markdown


def upload_location(instance, filename):
    return "{}/{}".format(instance.title, filename)


class PostManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)#('auth.User')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    # image = models.FileField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True, blank=True,
                              width_field='width_field',
                              height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    text = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    created_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    """
    you're going to allow a field to be blank in your form,
    you're going to also need your database to allow NULL values for that field.
    The exception is CharFields and TextFields, which in Django are never saved as NULL.
    Blank values are stored in the DB as an empty string ('').
    """

    objects = PostManager()

    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_markdown(self):
        text = self.text
        return mark_safe(markdown(text))

    class Meta:
        ordering = ['-created_date', 'title', ]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
