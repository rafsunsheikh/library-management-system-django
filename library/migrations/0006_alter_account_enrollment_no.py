# Generated by Django 4.0 on 2022-04-22 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_account_enrollment_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='enrollment_no',
            field=models.IntegerField(default=71870, unique=True),
        ),
    ]
