# Generated by Django 5.0.3 on 2024-03-25 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='restaurant_type',
            field=models.CharField(choices=[('IN', 'Indian'), ('CH', 'Chinese'), ('GR', 'Greek'), ('MX', 'Mexican'), ('FF', 'Fast Food'), ('OT', 'Other')], default='', max_length=2),
        ),
    ]