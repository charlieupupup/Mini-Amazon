from django.db import models

# Create your models here.
class stock(models.Model):
    # each record: one kind of products in one warehouse
    pid = models.IntegerField(default=-1) # product id
    count = models.IntegerField(default=-1) # product quantity
    worldid = models.IntegerField(default=-1)  # world id
    whid = models.IntegerField(default=-1)  # warehouse id

class warehouse(models.Model):
    whid = models.IntegerField(default=-1)  # warehouse id
    x = models.IntegerField(default=-1)  # warehouse address
    y = models.IntegerField(default=-1)  # warehouse address

class product(models.Model):
    pid = models.IntegerField(default=-1)  # product id
    description = models.CharField(max_length=1000, default="")  # product description
    catalog = models.IntegerField(default=-1)  # catalog id
    pic = models.CharField(max_length=1000, default="")  # product pic
    price = models.IntegerField(default=-1)  # product price