# Generated by Django 2.0 on 2018-01-30 13:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_auto_20180129_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_request',
            name='desc',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='leave_request',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 1, 30, 13, 52, 21, 252982, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rec',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 1, 30, 13, 52, 21, 251358, tzinfo=utc)),
        ),
    ]
