# Generated by Django 4.1.6 on 2023-02-10 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_photocontext_location_photocontext_people_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photocontext',
            name='date_link',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
