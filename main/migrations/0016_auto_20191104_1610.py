# Generated by Django 2.2.5 on 2019-11-04 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_invoicedetail_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicedetail',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6),
        ),
    ]