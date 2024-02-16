# Generated by Django 5.0.1 on 2024-02-05 15:01

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_comments_offers_auctionslistings'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionslistings',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionslistings',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 15, 1, 50, 333282, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='auctionslistings',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionslistings'),
        ),
        migrations.AddField(
            model_name='comments',
            name='comments',
            field=models.CharField(max_length=280, null=True),
        ),
        migrations.AddField(
            model_name='offers',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionslistings'),
        ),
        migrations.AddField(
            model_name='offers',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='auctionslistings',
            name='photo_url',
            field=models.URLField(blank=True),
        ),
    ]