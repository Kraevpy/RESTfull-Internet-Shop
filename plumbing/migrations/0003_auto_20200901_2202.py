# Generated by Django 3.1.1 on 2020-09-01 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plumbing', '0002_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
