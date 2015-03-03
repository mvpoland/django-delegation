# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DelegatedView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('pickled_request', models.TextField()),
                ('status_code', models.CharField(max_length=10, blank=True)),
                ('content_type', models.CharField(max_length=64, blank=True)),
                ('data_size', models.PositiveIntegerField(default=0)),
                ('data', models.FileField(null=True, upload_to=b'delegated_views/', blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
