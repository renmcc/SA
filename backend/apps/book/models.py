from django.db import models
from datetime import datetime

# Create your models here.


class uploadBook(models.Model):
    book = models.FileField(upload_to='books', verbose_name="文件上传")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    update_time = models.DateTimeField('更新时间', auto_now=True, help_text='更新时间')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '上传图书'
        verbose_name_plural = verbose_name