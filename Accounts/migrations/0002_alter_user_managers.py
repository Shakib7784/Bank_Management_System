# Generated by Django 4.2.1 on 2023-06-19 10:05

import Accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', Accounts.models.UserManager()),
            ],
        ),
    ]
