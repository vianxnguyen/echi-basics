# Generated by Django 3.2.6 on 2021-08-19 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0005_item_stock_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Pair', 'Pair'), ('Bundle', 'Bundle')], max_length=10),
        ),
    ]
