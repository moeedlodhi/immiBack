# Generated by Django 3.2 on 2023-06-05 15:57

import authentication.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20230602_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='random_name',
            field=authentication.fields.UpperStringField(blank=True, max_length=264, null=True),
        ),
    ]
