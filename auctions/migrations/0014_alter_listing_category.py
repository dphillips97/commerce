# Generated by Django 4.0.4 on 2022-07-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_bid_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('fashion', 'Fashion'), ('electronics', 'Electronics'), ('home', 'Home'), ('toys', 'Toys'), ('everything_else', 'Everything Else')], default=None, max_length=64, null=True),
        ),
    ]