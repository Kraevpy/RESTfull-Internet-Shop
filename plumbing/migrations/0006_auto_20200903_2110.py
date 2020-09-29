# Generated by Django 3.1.1 on 2020-09-03 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plumbing', '0005_auto_20200901_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('m', 'Maker'), ('i', 'Importer')], max_length=1)),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='certificate',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.DecimalField(decimal_places=5, max_digits=7),
        ),
        migrations.AlterField(
            model_name='product',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='serial_number',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='importer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plumbing.company'),
        ),
        migrations.AlterField(
            model_name='product',
            name='maker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maker', to='plumbing.company'),
        ),
        migrations.DeleteModel(
            name='Importer',
        ),
        migrations.DeleteModel(
            name='Maker',
        ),
    ]