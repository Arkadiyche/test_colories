# Generated by Django 3.2.5 on 2021-07-29 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calorie', '0005_auto_20210729_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='serving_weight',
            field=models.IntegerField(blank=True, verbose_name='Масса по умольчанию в граммах'),
        ),
        migrations.AlterField(
            model_name='personactivity',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.activity'),
        ),
        migrations.AlterField(
            model_name='personactivity',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.person'),
        ),
        migrations.AlterField(
            model_name='persondish',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.dish'),
        ),
        migrations.AlterField(
            model_name='persondish',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.person'),
        ),
    ]
