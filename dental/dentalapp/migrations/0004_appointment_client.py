# Generated by Django 5.1.1 on 2024-10-15 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dentalapp', '0003_alter_appointment_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='client',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
