# Generated by Django 3.2.5 on 2021-07-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorie', '0002_alter_activity_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='unit',
            field=models.CharField(max_length=150, verbose_name='Единица измерения'),
        ),
    ]