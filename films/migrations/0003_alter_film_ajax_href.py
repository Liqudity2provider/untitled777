# Generated by Django 3.2 on 2021-05-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_rename_my_field_name_film_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='ajax_href',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
