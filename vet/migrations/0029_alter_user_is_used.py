# Generated by Django 4.0.5 on 2022-08-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vet', '0028_alter_user_is_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
