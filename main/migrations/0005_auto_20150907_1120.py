# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_proxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='address',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
