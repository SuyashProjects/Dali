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

class Station1(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station2(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station3(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station4(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station5(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station6(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station7(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station8(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station9(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Station10(models.Model):
    SKU = models.ForeignKey(Config, on_delete=models.CASCADE,null=True)
    time = models.PositiveIntegerField(null=True)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.time)

class Shift(models.Model):
    name = models.CharField(max_length=10)
    time = models.PositiveIntegerField(null=True,default=8)
    def submit(self):
        self.save()
    def __str__(self):
        return str(self.name)
