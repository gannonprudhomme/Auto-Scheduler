# Generated by Django 2.1.7 on 2019-09-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0013_auto_20190928_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='building',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
