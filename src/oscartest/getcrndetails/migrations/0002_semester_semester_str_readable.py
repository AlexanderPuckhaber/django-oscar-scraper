# Generated by Django 3.1.4 on 2021-01-09 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getcrndetails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='semester_str_readable',
            field=models.CharField(default='Spring 2021', max_length=200),
            preserve_default=False,
        ),
    ]
