# Generated by Django 4.0.3 on 2022-08-08 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom_user',
            name='rate',
            field=models.IntegerField(default=0),
        ),
    ]
