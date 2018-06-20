from django.db import models
from django.utils import timezone

class  Config(models.Model):
    SKU = models.AutoField(primary_key=True)
    model = models.CharField(max_length=50)
    variant = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50,blank=True,null=True)
    time = models.IntegerField()
    constraints = models.CharField(max_length=50,null=True,blank=True)
    tank = models.CharField(max_length=50)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.SKU)
