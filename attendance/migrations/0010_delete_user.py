# Generated by Django 2.0 on 2018-01-12 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0009_auto_20180112_2336'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]