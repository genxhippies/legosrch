# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-29 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170929_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legoproductsku',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
