# Generated by Django 4.1.6 on 2023-02-10 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_transfer_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photocontext',
            name='date',
        ),
    ]
