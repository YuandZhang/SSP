# Generated by Django 3.1.2 on 2020-12-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SspModels',
            fields=[
                ('sspid', models.AutoField(primary_key=True, serialize=False)),
                ('xmpzh', models.CharField(max_length=100)),
                ('xmlb', models.CharField(max_length=30)),
                ('xkfl', models.CharField(max_length=50)),
                ('xmmc', models.CharField(max_length=300)),
                ('lxsj', models.DateField()),
                ('xmfzr', models.CharField(max_length=50)),
                ('zyzw', models.CharField(max_length=30)),
                ('gzdw', models.CharField(max_length=100)),
                ('dwlb', models.CharField(max_length=50)),
                ('szssq', models.CharField(max_length=100)),
                ('ssxt', models.CharField(max_length=100)),
            ],
        ),
    ]
