# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=512)),
                ('title', models.CharField(max_length=512)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=16)),
            ],
        ),
    ]
