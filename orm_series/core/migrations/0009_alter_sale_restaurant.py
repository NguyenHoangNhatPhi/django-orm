# Generated by Django 5.0.3 on 2024-03-28 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_restaurant_latitude_alter_restaurant_longitute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='core.restaurant'),
        ),
    ]
