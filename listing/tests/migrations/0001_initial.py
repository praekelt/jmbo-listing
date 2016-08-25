# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-24 17:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tests.BaseModel')),
            ],
            bases=('tests.basemodel',),
        ),
        migrations.CreateModel(
            name='TestWithTitleModel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tests.BaseModel')),
                ('title', models.CharField(max_length=32)),
            ],
            bases=('tests.basemodel',),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='basemodel_categories', to='category.Category'),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.Category'),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.Tag'),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='basemodel_tags', to='category.Tag'),
        ),
    ]
