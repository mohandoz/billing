# Generated by Django 2.2.5 on 2019-11-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20191113_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='folder_name',
            field=models.CharField(default='2', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='folder_name',
            field=models.CharField(max_length=30),
        ),
    ]
