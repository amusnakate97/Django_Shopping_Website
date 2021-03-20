from django.db import models

# Create your models here.
sizes = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
    )
class product(models.Model):

    id=models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    brand = models.CharField(max_length=200, null=True)
    price=models.SmallIntegerField()
    size = models.CharField(choices=sizes, max_length=20,default=sizes[0][0])
    img=models.ImageField(null=True)
    gender=models.CharField(max_length=200, null=True)

class cartItem(models.Model):
    user_id=models.CharField(max_length=200, null=True)
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    brand = models.CharField(max_length=200, null=True)
    price = models.SmallIntegerField()
    size = models.CharField(choices=sizes, max_length=20, default=sizes[0][0])
    img = models.ImageField(null=True)
    units=models.SmallIntegerField()
    ordered=models.BooleanField(default=False)
    removed=models.BooleanField(default=False)

