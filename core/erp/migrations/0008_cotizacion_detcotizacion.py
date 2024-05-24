# Generated by Django 5.0.4 on 2024-05-24 23:01

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0007_paymethods'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha Venta')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cli', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.clients', verbose_name='Cliente')),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.money', verbose_name='Moneda')),
                ('pay_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.paymethods', verbose_name='Método de Pago')),
            ],
            options={
                'verbose_name': 'Cotización',
                'verbose_name_plural': 'Cotizaciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=0, default=0.0, max_digits=9, verbose_name='Precio')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cotizacion', verbose_name='Venta')),
                ('repl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.replacement', verbose_name='Repuesto(s)')),
            ],
            options={
                'verbose_name': 'Detalle Cotización',
                'verbose_name_plural': 'Detalle Cotizaciones',
                'ordering': ['id'],
            },
        ),
    ]