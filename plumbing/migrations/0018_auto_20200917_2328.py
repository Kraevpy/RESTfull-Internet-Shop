# Generated by Django 3.1.1 on 2020-09-17 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plumbing', '0017_comments_send_data_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='products',
            field=models.ManyToManyField(blank=True, to='plumbing.Product'),
        ),
    ]
