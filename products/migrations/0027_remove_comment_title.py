# Generated by Django 4.0.3 on 2022-04-29 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_product_category_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
    ]
