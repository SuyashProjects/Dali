from django.db import models
from django.utils import timezone

class Config(models.Model):
 Status = (
  ('Queued', 'Queued'),
  ('Running', 'Running'),
  ('On Hold', 'On Hold'),
  ('Completed', 'Completed'),)
 SKU = models.AutoField(primary_key=True)
 model = models.CharField(max_length=6)
 variant = models.CharField(max_length=1)
 color = models.CharField(max_length=20)
 time = models.PositiveIntegerField(null=True)
 quantity = models.PositiveIntegerField(default=0)
 ratio = models.PositiveIntegerField(default=0)
 skips = models.BooleanField()
 strips = models.BooleanField()
 tank = models.CharField(max_length=10)
 description = models.CharField(max_length=50,default=None,blank=True,null=True)
 status = models.CharField(max_length=10, default='Queued', choices=Status)
 stn1 = models.PositiveIntegerField(default=0)
 stn2 = models.PositiveIntegerField(default=0)
 stn3 = models.PositiveIntegerField(default=0)
 stn4 = models.PositiveIntegerField(default=0)
 stn5 = models.PositiveIntegerField(default=0)
 stn6 = models.PositiveIntegerField(default=0)
 stn7 = models.PositiveIntegerField(default=0)
 stn8 = models.PositiveIntegerField(default=0)
 stn9 = models.PositiveIntegerField(default=0)
 stn10 = models.PositiveIntegerField(default=0)
 def submit(self):
  self.save()
 def __str__(self):
  return str(self.SKU)

class Seq(models.Model):
 Status = (
  ('Queued', 'Queued'),
  ('Running', 'Running'),
  ('On Hold', 'On Hold'),
  ('Completed', 'Completed'),)
 Sq_No = models.PositiveSmallIntegerField(default=0,primary_key=True)
 SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
 status = models.CharField(max_length=10, default='Queued', choices=Status)
 def submit(self):
  self.save()
 def __str__(self):
  return str(self.Sq_No)

class Shift(models.Model):
 name = models.CharField(max_length=5,unique=True)
 A = models.DecimalField(max_digits=5,decimal_places=2,default=7)
 B = models.DecimalField(max_digits=5,decimal_places=2,default=7)
 C = models.DecimalField(max_digits=5,decimal_places=2,default=7)
 def submit(self):
  self.save()
 def __str__(self):
  return str(self.name)
