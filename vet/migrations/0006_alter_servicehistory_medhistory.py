# Generated by Django 4.0.6 on 2022-07-09 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vet', '0005_services_is_vaccination_alter_breed_kind_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicehistory',
            name='medHistory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vet.medicalhistory', verbose_name='Medical History'),
        ),
    ]
