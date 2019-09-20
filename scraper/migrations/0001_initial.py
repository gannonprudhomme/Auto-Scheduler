# Generated by Django 2.2.5 on 2019-09-20 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('dept', models.CharField(db_index=True, max_length=4)),
                ('course_num', models.CharField(db_index=True, max_length=5)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('prerequisites', models.TextField(blank=True, null=True)),
                ('corequisites', models.TextField(blank=True, null=True)),
                ('min_credits', models.FloatField(null=True)),
                ('max_credits', models.FloatField(null=True)),
                ('distribution_of_hours', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=100)),
            ],
        ),
    ]
