# Generated by Django 3.1.2 on 2021-03-02 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210302_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenditure',
            name='remarks',
            field=models.CharField(max_length=1000, null=True, verbose_name='Remarks'),
        ),
    ]
