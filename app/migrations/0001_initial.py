# Generated by Django 4.0.5 on 2022-08-17 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResultsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propozycja_1', models.IntegerField()),
                ('propozycja_2', models.IntegerField()),
                ('propozycja_3', models.IntegerField()),
            ],
        ),
    ]