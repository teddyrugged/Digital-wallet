# Generated by Django 4.0.4 on 2022-04-19 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_rate_base_quote_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='base_quote_symbol',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
