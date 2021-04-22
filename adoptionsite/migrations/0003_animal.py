# Generated by Django 3.1.7 on 2021-03-30 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adoptionsite', '0002_auto_20210331_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=50)),
                ('age', models.IntegerField(default=0)),
            ],
        ),
    ]
