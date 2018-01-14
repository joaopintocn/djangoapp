# Generated by Django 2.0 on 2018-01-11 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_staff_category_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='department',
            field=models.CharField(choices=[('BT', 'BioTechnology'), ('CSE', 'Computer Science'), ('EC', 'Electronics and Communication'), ('MECH', 'Mechanical'), ('APPL', 'Applied Science'), ('LIB', 'Library'), ('ADM', 'Administration'), ('OTH', 'Others')], default='OTH', max_length=5),
        ),
        migrations.AddField(
            model_name='staff',
            name='joining_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='staff',
            name='qualification',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='staff',
            name='termination_date',
            field=models.DateTimeField(blank=True, default=None),
        ),
    ]