# Generated by Django 5.0.3 on 2024-03-25 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_restaurant_restaurant_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='core.restaurant'),
        ),
    ]