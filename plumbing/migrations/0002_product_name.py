# Generated by Django 3.1.1 on 2020-09-01 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plumbing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]