from django.db import models
from django.utils import timezone

class Constraint(models.Model):
    name = models.CharField(max_length=100)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)

class Config(models.Model):
    Status = (
        ('Queued', 'Queued'),
        ('Running', 'Running'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
    )
    SKU = models.AutoField(primary_key=True)
    model = models.CharField(max_length=6)
    variant = models.CharField(max_length=1)
    color = models.CharField(max_length=20)
    time = models.PositiveIntegerField(null=True)
    quantity = models.PositiveIntegerField(default=0)
    ratio = models.PositiveIntegerField(default=0)
    constraints = models.ManyToManyField(Constraint, related_name='Constraint',blank=True)
    tank = models.CharField(max_length=10)
    description = models.CharField(max_length=50,default=None,blank=True,null=True)
    status = models.CharField(max_length=10, default='Queued', choices=Status)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.SKU)

class Seq(models.Model):
    Sq_No = models.PositiveSmallIntegerField(default=0)
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.SKU)

class Station(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE)
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

class Shift(models.Model):
    name = models.CharField(max_length=5)
    time = models.PositiveIntegerField(default=7)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)
