# Generated by Django 4.0.3 on 2022-03-24 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_discount_discount_item'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Discount_item',
        ),
    ]
