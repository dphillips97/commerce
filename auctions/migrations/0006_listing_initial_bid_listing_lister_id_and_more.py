# Generated by Django 4.0.4 on 2022-07-20 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='initial_bid',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AddField(
            model_name='listing',
            name='lister_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('C', 'Clothing'), ('E', 'Electronics'), ('EE', 'Everything')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, max_length=512),
        ),
    ]
