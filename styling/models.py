from django.db import models
from django.utils import timezone
from divas.models.user import Users


class Styling(models.Model):
    username=models.ForeignKey(Users, on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)
    photo= models.ManyToManyField('Photos')
    created=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)

class Photos(models.Model):
    photos=models.ImageField(upload_to='photos/')
    submission=models.ManyToManyField(Styling)
    productId=models.CharField(verbose_name='Product Name', max_length=100,default='')
    
class Products(models.Model):
    photos=models.ImageField(upload_to='photos/')
