# Generated by Django 4.0.3 on 2022-07-02 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_alter_order_items_qunatity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25)),
                ('price', models.DecimalField(decimal_places=0, max_digits=9)),
            ],
        ),
        migrations.AlterField(
            model_name='order_items',
            name='qunatity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.delivery'),
        ),
    ]