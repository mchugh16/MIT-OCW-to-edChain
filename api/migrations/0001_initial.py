# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.TextField()),
                ('instructors', models.TextField()),
                ('version', models.CharField(max_length=50)),
                ('level', models.CharField(max_length=50)),
                ('chp_image', models.ImageField(upload_to='')),
                ('chp_image_caption', models.TextField()),
                ('course_description', models.TextField()),
                ('course_features', models.TextField()),
            ],
        ),
    ]
