# Generated by Django 2.1.7 on 2019-09-28 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0018_auto_20190928_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='currentEnrolled',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='section',
            name='maxEnrollment',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
