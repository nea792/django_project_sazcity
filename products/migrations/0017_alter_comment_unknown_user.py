# Generated by Django 4.0.3 on 2022-04-02 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_discount_percent_alter_product_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='unknown_user',
            field=models.BinaryField(max_length='max'),
        ),
    ]
