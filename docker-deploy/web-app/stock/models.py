from django.db import models

# Create your models here.
class stock(models.Model):
    pid = models.IntegerField(default=-1) # product id
    description = models.CharField(max_length=1000, default="") # product description
    count = models.IntegerField(default=-1) # product quantity
    worldid = models.IntegerField(default=-1)  # world id
    whnum = models.IntegerField(default=-1)  # warehouse id
