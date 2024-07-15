from django.db import models


class Users(models.Model):
    username=models.CharField(max_length=100,unique=True)
    followers=models.IntegerField()
    ranking=models.IntegerField()
    about=models.TextField()
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


   