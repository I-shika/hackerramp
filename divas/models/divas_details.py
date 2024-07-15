from django.db import models
from django.utils import timezone
from .user import Users

class Divas(models.Model):
    username=models.ForeignKey(Users, verbose_name=_(""), on_delete=models.CASCADE)
    overall_ranking=models.BigIntegerField(verbose_name="Overall Rating")
    followers=models.BigIntegerField(verbose_name="followers")
    following=models.BigIntegerField(verbose_name="following")
    created=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()

        self.updated = timezone.now()
        return super(Divas, self).save(*args, **kwargs)
    class Meta:
        
        verbose_name_plural = "divas"



