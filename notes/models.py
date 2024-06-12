from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200,null=True)
    description = models.TextField(null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title