# Generated by Django 4.0.4 on 2022-07-10 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('item_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('image_url', models.URLField(blank=True)),
                ('active', models.BooleanField()),
            ],
        ),
    ]
