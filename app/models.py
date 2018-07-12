from django.db import models
from django.utils import timezone

class Constraint(models.Model):
    name = models.CharField(max_length=100)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)

class Config(models.Model):
    SKU = models.AutoField(primary_key=True)
    model = models.CharField(max_length=6)
    variant = models.CharField(max_length=1)
    color = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(blank=True,null=True)
    time = models.PositiveIntegerField(null=True)
    ratio = models.PositiveIntegerField(default=0,null=True)
    constraints = models.ManyToManyField(Constraint, related_name='Constraint',blank=True)
    tank = models.CharField(max_length=10)
    description = models.CharField(max_length=50,default=None,blank=True,null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.SKU)

class Station(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE)
    stn1 = models.PositiveIntegerField(default=0,null=True)
    stn2 = models.PositiveIntegerField(default=0,null=True)
    stn3 = models.PositiveIntegerField(default=0,null=True)
    stn4 = models.PositiveIntegerField(default=0,null=True)
    stn5 = models.PositiveIntegerField(default=0,null=True)
    stn6 = models.PositiveIntegerField(default=0,null=True)
    stn7 = models.PositiveIntegerField(default=0,null=True)
    stn8 = models.PositiveIntegerField(default=0,null=True)
    stn9 = models.PositiveIntegerField(default=0,null=True)
    stn10 = models.PositiveIntegerField(default=0,null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.SKU)

class Shift(models.Model):
    name = models.CharField(max_length=5)
    time = models.PositiveIntegerField(null=True,default=7)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)
