# Generated by Django 4.1.2 on 2023-01-03 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_ordermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='paymentVia',
            field=models.CharField(default='', max_length=50),
        ),
    ]
