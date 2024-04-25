# Generated by Django 5.0.4 on 2024-04-25 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_category_date_creation_category_date_updated_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_replacement', models.CharField(max_length=150, null=True, unique=True, verbose_name='Código')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='Nombre')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock')),
                ('pvp', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio Final')),
                ('location', models.CharField(blank=True, max_length=150, null=True, verbose_name='Ubicación')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.category', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Repuestos',
                'verbose_name_plural': 'Repuestos',
                'ordering': ['id'],
            },
        ),
    ]
