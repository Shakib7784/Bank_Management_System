# Generated by Django 4.2.1 on 2023-06-19 10:01

import Accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('maximum_withdrawal_amount', models.DecimalField(decimal_places=2, max_digits=11)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', Accounts.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.PositiveIntegerField(unique=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('initial_deposite_date', models.DateField(blank=True, null=True)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='Accounts.bankaccounttype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='BankAccount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=250)),
                ('postal_code', models.PositiveIntegerField()),
                ('country', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
