from django.contrib import admin

from .models import Category, AuctionsListings, Comments, Bids
# Register your models here.

admin.site.register(Category)
admin.site.register(AuctionsListings)
admin.site.register(Comments)
admin.site.register(Bids)