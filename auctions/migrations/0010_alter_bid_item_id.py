# Generated by Django 4.0.4 on 2022-07-24 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
