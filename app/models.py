from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only Alphanumeric characters are allowed.')
Calphabets = RegexValidator(r'^[A-Z]*$', 'Only Capital Alphabets are allowed.')
alphabets = RegexValidator(r'^[a-zA-Z]*$', 'Only Alphabets are allowed.')

class Config(models.Model):
 Status = (
  ('Queued', 'Queued'),
  ('Running', 'Running'),
  ('On Hold', 'On Hold'),
  ('Completed', 'Completed'),)
 SKU = models.AutoField(primary_key=True)
 model = models.CharField(max_length=6,validators=[alphanumeric])
 variant = models.CharField(max_length=1,validators=[Calphabets])
 color = models.CharField(max_length=15,validators=[alphabets])
 time = models.PositiveIntegerField(null=True)
 quantity = models.PositiveIntegerField(default=0)
 ratio = models.PositiveIntegerField(default=0)
 skips = models.BooleanField(default=False)
 strips = models.BooleanField(default=False)
 tank = models.CharField(max_length=10,validators=[alphabets])
 description = models.CharField(max_length=25,default=None,blank=True,null=True,validators=[alphabets])
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
 def save(self, *args, **kwargs):
  self.stn1 = self.time
  self.stn2 = self.time
  self.stn3 = self.time
  self.stn4 = self.time
  self.stn5 = self.time
  self.stn6 = self.time
  self.stn7 = self.time
  self.stn8 = self.time
  self.stn9 = self.time
  self.stn10 = self.time
  super(Config, self).save(*args, **kwargs) # Call the "real" save() method.


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
