# Generated by Django 2.2.2 on 2019-06-11 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20181115_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='partner.Currency'),
        ),
    ]
