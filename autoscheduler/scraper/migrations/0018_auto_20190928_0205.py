# Generated by Django 2.1.7 on 2019-09-28 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0017_auto_20190928_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='currentEnrolled',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='maxEnrollment',
            field=models.IntegerField(null=True),
        ),
    ]
