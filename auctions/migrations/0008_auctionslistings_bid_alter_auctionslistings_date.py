# Generated by Django 5.0.1 on 2024-02-15 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comments_user_alter_auctionslistings_date_bids_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionslistings',
            name='bid',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='auctionslistings',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 15, 17, 6, 10, 338662, tzinfo=datetime.timezone.utc)),
        ),
    ]
