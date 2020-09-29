# Generated by Django 3.1.1 on 2020-09-03 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plumbing', '0007_auto_20200903_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='child',
            field=models.ManyToManyField(to='plumbing.Category'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_field', to='plumbing.category'),
        ),
    ]
