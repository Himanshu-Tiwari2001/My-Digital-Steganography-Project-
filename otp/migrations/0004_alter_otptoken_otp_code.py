# Generated by Django 5.0.4 on 2024-05-18 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0003_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='ed4394', max_length=6),
        ),
    ]
