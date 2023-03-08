# Generated by Django 4.1.7 on 2023-03-08 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks_pipeline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('pipeline', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks_pipeline.pipeline')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, editable=False, max_length=30, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField()),
                ('price', models.FloatField()),
                ('seller_commission_tax', models.FloatField()),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.producttype')),
            ],
        ),
    ]
