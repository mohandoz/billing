# Generated by Django 2.2.5 on 2019-10-31 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20191031_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialorder',
            name='invoice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='material_orders', to='main.Invoice'),
            preserve_default=False,
        ),
    ]
