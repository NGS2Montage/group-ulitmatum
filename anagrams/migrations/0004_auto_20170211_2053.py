# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 20:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anagrams', '0003_lettertransaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lettertransaction',
            old_name='borrowor',
            new_name='borrower',
        ),
    ]
