# Generated by Django 5.0.1 on 2024-02-08 19:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auctionslistings_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionslistings',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 8, 19, 47, 26, 583710, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='auctionslistings',
            name='title',
            field=models.CharField(max_length=45),
        ),
    ]
