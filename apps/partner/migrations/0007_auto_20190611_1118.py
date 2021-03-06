# Generated by Django 2.2.2 on 2019-06-11 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'Currencies'},
        ),
        migrations.RemoveField(
            model_name='currency',
            name='id',
        ),
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=6, max_digits=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('base_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_currencies', to='partner.Currency')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Currency')),
            ],
        ),
    ]
