# Generated by Django 4.0.3 on 2022-04-04 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_alter_comment_unknown_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='liked',
        ),
    ]