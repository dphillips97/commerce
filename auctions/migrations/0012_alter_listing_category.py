# Generated by Django 4.0.4 on 2022-07-25 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_bid_amount_alter_listing_initial_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('C', 'Clothing'), ('E', 'Electronics'), ('EE', 'Everything Else')], default=None, max_length=2, null=True),
        ),
    ]
