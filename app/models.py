from django.db import models
from django.utils import timezone

class Constraint(models.Model):
    name = models.CharField(max_length=100)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)

class Station(models.Model):
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Config(models.Model):
    SKU = models.AutoField(primary_key=True)
    Station = models.ManyToManyField(Station, null=True)
    model = models.CharField(max_length=50)
    variant = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(blank=True,null=True)
    time = models.PositiveIntegerField(null=True)
    ratio = models.IntegerField(null=True)
    constraints = models.ManyToManyField(Constraint, related_name='Constraint',blank=True)
    tank = models.CharField(max_length=50)
    description = models.CharField(max_length=100,default=None,blank=True,null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.SKU)

class Shift(models.Model):
    name = models.CharField(max_length=10)
    time = models.PositiveIntegerField(null=True,default=8)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)
