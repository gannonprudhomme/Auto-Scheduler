# Generated by Django 2.1.7 on 2019-09-23 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_auto_20190922_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='id',
            new_name='crn',
        ),
    ]
