# Generated by Django 2.2.5 on 2019-11-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_invoice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=30, verbose_name='اسم الفرع'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'فعال'), (2, 'غير فعال')], default=1),
        ),
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'فعال'), (2, 'غير فعال')], default=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'فعال'), (2, 'غير فعال')], default=1),
        ),
        migrations.AlterField(
            model_name='material',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'فعال'), (2, 'غير فعال')], default=1),
        ),
    ]