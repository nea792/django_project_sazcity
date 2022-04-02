# Generated by Django 4.0.3 on 2022-03-28 12:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0014_alter_comment_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='liked',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]