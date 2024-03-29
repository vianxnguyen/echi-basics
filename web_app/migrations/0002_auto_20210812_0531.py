# Generated by Django 3.2.6 on 2021-08-12 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='item',
            name='label',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('P', 'Pair'), ('B', 'Bundle')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(default='test description'),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=100)),
        ),
    ]
