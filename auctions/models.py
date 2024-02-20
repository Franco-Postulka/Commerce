from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

class AuctionsListings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='owner') 
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=125) 
    price = models.IntegerField()
    bid = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=True)
    # Optionals
    photo_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    watchlist = models.ManyToManyField(User,blank=True, related_name='watchlist')
    winner = models.ManyToManyField(User,blank=True,related_name="winer")

class Bids(models.Model):
    auction = models.ForeignKey(AuctionsListings,on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Comments(models.Model):
    auction = models.ForeignKey(AuctionsListings,on_delete=models.CASCADE,  null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=200, null=True) 


