# Generated by Django 3.1.1 on 2020-09-04 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plumbing', '0009_auto_20200903_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='child',
        ),
    ]
