# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150829_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='maindata',
            name='body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
