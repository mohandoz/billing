# Generated by Django 2.2.5 on 2019-11-13 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20191113_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='folder_name',
        ),
        migrations.AddField(
            model_name='branch',
            name='folder_path',
            field=models.CharField(default=' ', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='folder_path',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]