# Generated by Django 2.1.3 on 2018-12-07 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0002_auto_20181206_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='comicstrip',
            name='scraper_name',
            field=models.CharField(choices=[('default', 'Default'), ('invisible_bread', 'Invisible Bread')], default='default', max_length=100),
        ),
    ]
