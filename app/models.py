from django.db import models
from django.utils import timezone

class Constraint(models.Model):
    name = models.CharField(max_length=100)
    shift_time = models.IntegerField(default=8)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)

class Config(models.Model):
    SKU = models.AutoField(primary_key=True)
    model = models.CharField(max_length=50)
    variant = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    quantity = models.IntegerField(blank=True,null=True)
    time = models.IntegerField(null=True)
    constraints = models.ManyToManyField(Constraint, related_name='Constraint',blank=True)
    tank = models.CharField(max_length=50)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.SKU)
