# Generated by Django 2.2.5 on 2019-11-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20191113_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='folder_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
