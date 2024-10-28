from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from photo.fields import  ThumbnailGifField

class Category(models.Model):
    name = models.CharField("Category name", max_length=200, unique=True)

    # __str__를 사용해서 추후 해당 테이블을 불러올때 보여줄 값을 지정할 수 있다.
    def __str__(self):
        return self.name


class GifArchive(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='OWNER')
    name = models.CharField('GIF Name', max_length=255, blank=False, null=False)
    gif_image = ThumbnailGifField(upload_to='photo/%Y/%m')
    create_dt = models.DateField(auto_now_add=True)
    modify_dt = models.DateField(auto_now=True)

    def days_since_modified(self):
        current_date = timezone.now().date()
        df = (current_date - self.modify_dt).days
        return df

    class Meta:
        ordering = ('-modify_dt',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=(self.id,))
    
    def delete(self, using=None, keep_parents=False):
        self.gif_image.delete(save=False)

        super().delete(using=using, keep_parents=keep_parents)

class Like(models.Model):
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='liker')
    gif = models.ForeignKey(GifArchive, on_delete=models.CASCADE, verbose_name='gif_image')

    class Meta:
        # One user can only like one gif once
        unique_together = ('liker', 'gif')
    
    def __str__(self):
        return f"{self.liker} - {self.gif}"