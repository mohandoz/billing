# Generated by Django 2.2.5 on 2019-11-13 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20191113_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoicedetail',
            options={'ordering': ['material']},
        ),
        migrations.AddField(
            model_name='company',
            name='folder_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]