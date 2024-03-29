# Generated by Django 2.2.5 on 2019-11-03 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20191103_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='material',
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_details', to='main.Invoice'),
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_details', to='main.Material'),
        ),
    ]
