# Generated by Django 4.0.4 on 2022-04-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_remove_rate_base_currency_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
