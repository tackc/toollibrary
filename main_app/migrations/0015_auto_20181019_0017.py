# Generated by Django 2.1.1 on 2018-10-19 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_auto_20181019_0000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='toolrating',
            old_name='tool',
            new_name='tools',
        ),
    ]