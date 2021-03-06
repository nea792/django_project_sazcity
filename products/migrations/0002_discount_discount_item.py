# Generated by Django 4.0.3 on 2022-03-24 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Discount_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.discount')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
