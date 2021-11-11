# Generated by Django 3.2.9 on 2021-11-11 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]