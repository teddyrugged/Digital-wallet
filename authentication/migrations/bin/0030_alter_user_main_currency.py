# Generated by Django 4.0.4 on 2022-04-25 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0029_alter_user_main_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='main_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.currency'),
        ),
    ]