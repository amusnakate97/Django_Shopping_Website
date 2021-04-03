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
    status=models.CharField(max_length=200, null=True)

class Profile(models.Model):
    user_id=models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='images')
    address=models.CharField(max_length=2000, null=True)

class Review(models.Model):
    review_id=models.SmallIntegerField(primary_key=True)
    review = models.CharField(max_length=200, null=True)
    item_id=models.SmallIntegerField()
    user_id=models.CharField(max_length=200, null=True)