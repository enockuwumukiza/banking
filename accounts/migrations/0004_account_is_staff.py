# Generated by Django 5.1.4 on 2024-12-12 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]