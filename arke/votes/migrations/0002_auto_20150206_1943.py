# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='extra_description',
            field=models.TextField(max_length=4096),
            preserve_default=True,
        ),
    ]
