# Generated by Django 4.0.3 on 2022-08-01 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_remove_category_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(auto_now=True),
        ),
    ]