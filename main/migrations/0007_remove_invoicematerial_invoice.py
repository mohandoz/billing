# Generated by Django 2.2.5 on 2019-10-31 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20191031_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicematerial',
            name='invoice',
        ),
    ]
