# Generated by Django 4.0.4 on 2022-04-25 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0030_alter_user_main_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='main_currency',
            field=models.CharField(max_length=100),
        ),
    ]
