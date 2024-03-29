# Generated by Django 5.0.1 on 2024-02-17 14:32

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionslistings_bid_alter_auctionslistings_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionslistings',
            name='winner',
            field=models.ManyToManyField(blank=True, related_name='winer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionslistings',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 17, 14, 32, 23, 230290, tzinfo=datetime.timezone.utc)),
        ),
    ]
