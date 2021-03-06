# Generated by Django 2.0 on 2018-02-07 15:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0018_auto_20180130_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_request',
            name='department',
            field=models.CharField(choices=[('BT', 'BioTechnology'), ('CSE', 'Computer Science'), ('EC', 'Electronics and Communication'), ('MECH', 'Mechanical'), ('APPL', 'Applied Science'), ('LIB', 'Library'), ('ADM', 'Administration'), ('OTH', 'Others')], default='OTH', max_length=5),
        ),
        migrations.AlterField(
            model_name='leave_request',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 2, 7, 15, 34, 23, 280250, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leave_request',
            name='desc',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='rec',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 2, 7, 15, 34, 23, 278539, tzinfo=utc)),
        ),
    ]
