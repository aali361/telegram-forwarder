# Generated by Django 2.2.15 on 2020-08-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_account_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='task_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]