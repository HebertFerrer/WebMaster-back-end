# Generated by Django 2.2 on 2019-06-08 02:27

import apps.utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalificationToProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('stars', models.DecimalField(decimal_places=1, max_digits=2, validators=[apps.utils.validators.reputation_validator])),
                ('comment', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]