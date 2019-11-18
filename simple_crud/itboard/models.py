from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('created_ts',)


def image_file(instance, filename):
    return '/'.join(('images', f"{str(instance.post_id)}_{filename}"))


class Image(BaseModel):
    post = models.ForeignKey('Post', related_name='images', on_delete=models.CASCADE)
    file = models.ImageField(upload_to=image_file, blank=False, null=False)

    class Meta:
        db_table = 'sc_image'


class Post(BaseModel):
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=127, default='')
    text = models.TextField()

    class Meta:
        db_table = 'sc_post'
